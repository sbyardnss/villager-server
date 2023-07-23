from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.contrib.contenttypes.models import ContentType

from villager_chess_api.models import Tournament, Player, TimeSetting, Game, GuestPlayer, ChessClub


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name')


class GuestPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'full_name', 'guest_id')


class ClubOnTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ('id', 'name')
# class GameTournamentSerializer(serializers.ModelSerializer):
#     player_w = PlayerSerializer(many=False)
#     player_b = PlayerSerializer(many=False)
#     class Meta:
#         model = Game
#         # fields = ('id', 'player_w', 'player_b', 'winner', 'pgn', 'win_style', 'tournament_round')
#         fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
#                   'is_tournament', 'time_setting', 'winner', 'pgn', 'bye', 'accepted')


# added during scorecard function creation. I dont believe we need this permanently
class PlayerObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, GuestPlayer):
            serializer = GuestPlayerSerializer(value, many=False)
        elif isinstance(value, Player):
            serializer = PlayerSerializer(value, many=False)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data


class GameTournamentSerializer(serializers.ModelSerializer):
    player_w = PlayerObjectRelatedField(many=False, read_only=True)
    player_b = PlayerObjectRelatedField(many=False, read_only=True)
    winner = PlayerObjectRelatedField(many=False, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
                  'time_setting', 'winner', 'pgn', 'bye', 'accepted', 'win_style', 'target_winner_ct', 'target_player_b_ct', 'target_player_w_ct')  # removed target_winner_ct, target_player_b_ct, target_player_w_ct


class TournamentSerializer(serializers.ModelSerializer):
    creator = PlayerSerializer(many=False)
    # games = GameTournamentSerializer(many=True)
    competitors = PlayerSerializer(many=True)
    guest_competitors = GuestPlayerSerializer(many=True)
    club = ClubOnTournamentSerializer(many=False)

    class Meta:
        model = Tournament
        fields = ('id', 'title', 'creator', 'games', 'time_setting',
                  'complete', 'competitors', 'guest_competitors', 'rounds', 'pairings', 'in_person', 'club')


class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'title', 'time_setting', 'pairings', 'in_person', 'club']


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
                        competitors=competitor_list, guest_competitors=guest_competitor_list)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """handles PUT requests for tournament view"""
        tournament = Tournament.objects.get(pk=pk)
        tournament.rounds = request.data['rounds']
        tournament.pairings = request.data['pairings']
        tournament.competitors.set(request.data['competitors'])
        tournament.guest_competitors.set(request.data['guest_competitors'])
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def my_tournaments(self, request):
        player = Player.objects.get(user=request.auth.user)
        tournaments = Tournament.objects.filter(competitors=player)
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def end_tournament(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        tournament.complete = True
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def score_card(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        scorecard = {}
        tournament_games = Game.objects.filter(tournament=pk)
        # for game in tournament_games:
        #     # this gives me the player who won
        #     print(game.winner) 
        for player in tournament.competitors.all():
            scorecard[player.id] = []
            player_obj = Player.objects.get(pk=player.id)
            ct_id = ContentType.objects.get_for_model(Player)
            player_games = tournament_games.filter(Q(target_player_w_ct = ct_id, target_player_w_id = player.id) | Q(target_player_b_ct = ct_id, target_player_b_id = player.id))
            # 3 lines below work for getting winner of game
            # round = 1
            # round_one_player_game = player_games.filter(tournament_round = round)
            # print(round_one_player_game[0].winner)

            # iterating rounds
            for round in range(tournament.rounds):
                round_player_game = player_games.filter(tournament_round = round+1)
                # check if game exists
                if round_player_game:
                    # check if bye game
                    if round_player_game.first().bye == True:
                        scorecard[player.id].append('bye')
                    else:
                    # check if player won
                        if round_player_game.first().winner == player_obj:
                            scorecard[player.id].append(1)
                        # check if draw
                        elif round_player_game.first().win_style == 'draw':
                            scorecard[player.id].append(.5)
                        # if not winner and not draw then player lost
                        else:
                            scorecard[player.id].append(0)
                else:
                    scorecard[player.id].append('none')
        for guest in tournament.guest_competitors.all():
            scorecard[guest.guest_id] = []
            guest_obj = GuestPlayer.objects.get(pk=guest.id)
            ct_id = ContentType.objects.get_for_model(GuestPlayer)
            player_games = tournament_games.filter(Q(target_player_w_ct = ct_id, target_player_w_id = guest.id) | Q(target_player_b_ct = ct_id, target_player_b_id = guest.id))
            # 3 lines below work for getting winner of game
            # round = 1
            # round_one_player_game = player_games.filter(tournament_round = round)
            # print(round_one_player_game[0].winner)

            # iterating rounds
            for round in range(tournament.rounds):
                round_player_game = player_games.filter(tournament_round = round+1)
                # check if game exists
                if round_player_game:
                    # check if bye game
                    if round_player_game.first().bye == True:
                        scorecard[guest.guest_id].append('bye')
                    # check if player won
                    else:
                        if round_player_game.first().winner == guest_obj:
                            scorecard[guest.guest_id].append(1)
                        # check if draw
                        elif round_player_game.first().win_style == 'draw':
                            # print(round_player_game.first().win_style)
                            scorecard[guest.guest_id].append(.5)
                        # if not winner and not draw then player lost
                        else:
                            scorecard[guest.guest_id].append(0)
                else:
                    scorecard[guest.guest_id].append('none')
        return Response(scorecard, status=status.HTTP_200_OK)
