from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action

from villager_chess_api.models import Tournament, Player, TimeSetting, Game, GuestPlayer


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name')

class GuestPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'full_name', 'guest_id')

class GameTournamentSerializer(serializers.ModelSerializer):
    player_w = PlayerSerializer(many=False)
    player_b = PlayerSerializer(many=False)
    class Meta:
        model = Game
        # fields = ('id', 'player_w', 'player_b', 'winner', 'pgn', 'win_style', 'tournament_round')
        fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
                  'is_tournament', 'time_setting', 'winner', 'pgn', 'bye', 'accepted')


class TournamentSerializer(serializers.ModelSerializer):
    creator = PlayerSerializer(many=False)
    # games = GameTournamentSerializer(many=True)
    guest_competitors = GuestPlayerSerializer(many=True)
    class Meta:
        model = Tournament
        fields = ('id', 'title', 'creator', 'games', 'time_setting',
                  'complete', 'competitors', 'guest_competitors', 'rounds', 'pairings', 'in_person')


class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'title', 'time_setting', 'pairings', 'in_person']


class TournamentView(ViewSet):
    """handles rest requests for tournament objects"""

    def list(self, request):
        """handles GET requests for all tournaments"""
        tournaments = Tournament.objects.all()
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """handles GET requests for single tournament"""
        tournament = Tournament.objects.get(pk=pk)
        serialized = TournamentSerializer(tournament, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """handles POST requests for tournament view"""
        creator = Player.objects.get(user=request.auth.user)
        time_setting = TimeSetting.objects.get(pk=request.data['timeSetting'])
        competitor_list = request.data['competitors']
        guest_competitor_list = request.data['guest_competitors']
        serialized = CreateTournamentSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(creator=creator, time_setting=time_setting,
                        competitors=competitor_list, guest_competitors = guest_competitor_list)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """handles PUT requests for tournament view"""
        tournament = Tournament.objects.get(pk=pk)
        tournament.rounds = request.data['rounds']
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['get'], detail=False)
    def my_tournaments(self, request):
        player = Player.objects.get(user = request.auth.user)
        tournaments = Tournament.objects.filter(competitors = player)
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    @action(methods=['put'], detail=True)
    def end_tournament(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        tournament.complete = True
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)