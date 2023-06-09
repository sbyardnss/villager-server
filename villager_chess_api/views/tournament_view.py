from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
# from rest_framework.decorators import action
# from datetime import datetime
# from django.db.models import Count, Q
# from django.contrib.auth.models import User
from villager_chess_api.models import Tournament, Player, TimeSetting, Game

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name')
class GameTournamentSerializer(serializers.ModelSerializer):
    player_w = PlayerSerializer(many=False)
    player_b = PlayerSerializer(many=False)
    class Meta:
        model = Game
        fields = ('id', 'player_w', 'player_b', 'winner', 'pgn', 'win_style', 'tournament_round')
class TournamentSerializer(serializers.ModelSerializer):
    creator = PlayerSerializer(many=False)
    games = GameTournamentSerializer(many=True)
    class Meta:
        model = Tournament
        fields = ('id', 'title', 'creator', 'games', 'time_setting', 'complete')
class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'title', 'time_setting']
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
        creator = Player.objects.get(user = request.auth.user)
        time_setting = TimeSetting.objects.get(pk=request.data['timeSetting'])
        serialized = CreateTournamentSerializer(data = request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(creator = creator, time_setting = time_setting)
        return Response(serialized.data, status=status.HTTP_201_CREATED)