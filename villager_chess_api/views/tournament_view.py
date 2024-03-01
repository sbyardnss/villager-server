from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from villager_chess_api.models import Tournament, Player, TimeSetting, Game, GuestPlayer, ChessClub
from villager_chess_api.serializers import TournamentSerializer, CreateTournamentSerializer
import json
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
        # competitor_list = request.data['competitors']
        competitor_list = [competitor['id'] for competitor in request.data['competitors']]
        # guest_competitor_list = request.data['guest_competitors']
        guest_competitor_list = [guest['id'] for guest in request.data['guest_competitors']]

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
        # tournament.competitors.set(request.data['competitors'])
        competitor_ids = [competitor['id'] for competitor in request.data['competitors']]
        competitors = Player.objects.filter(id__in=competitor_ids)
        tournament.competitors.set(competitors)
        # tournament.guest_competitors.set(request.data['guest_competitors'])
        guest_competitor_ids = [guest['id'] for guest in request.data['guest_competitors']]
        guest_competitors = GuestPlayer.objects.filter(id__in=guest_competitor_ids)
        tournament.guest_competitors.set(guest_competitors)
        # print(json.dumps(TournamentSerializer(tournament, many=False).data, indent=4))
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        tourney_games = Game.objects.filter(tournament = tournament.id)
        for game in tourney_games:
            game.delete()
        tournament.competitors.set([])
        tournament.guest_competitors.set([])
        tournament.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=False)
    def my_tournaments(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.filter(members=player)
        tournaments = Tournament.objects.filter(club__in=clubs)
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def my_open_tournaments(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.filter(members=player)
        tournaments = Tournament.objects.filter(club__in=clubs, complete=False)
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def my_past_tournaments(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.filter(members=player)
        tournaments = Tournament.objects.filter(club__in=clubs, complete=True)
        serialized = TournamentSerializer(tournaments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


    @action(methods=['put'], detail=True)
    def end_tournament(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        tournament.complete = True
        tournament.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def reopen_tournament(self, request, pk=None):
        tournament = Tournament.objects.get(pk=pk)
        tournament.complete = False
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
