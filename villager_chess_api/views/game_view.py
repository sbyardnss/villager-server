from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Player, Game, Tournament, TimeSetting


class PlayerOnGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name')


class GameSerializer(serializers.ModelSerializer):
    player_w = PlayerOnGameSerializer(many=False)
    player_b = PlayerOnGameSerializer(many=False)
    winner = PlayerOnGameSerializer(many=False)

    class Meta:
        model = Game
        fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
                  'is_tournament', 'time_setting', 'winner', 'pgn', 'bye')


class CreateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['id', 'date_time', 'is_tournament',
                  'time_setting', 'tournament', 'win_style', 'winner', 'accepted', 'tournament_round', 'bye']

class GameView(ViewSet):
    """handles rest requests for game objects"""

    def list(self, request):
        """handles GET requests for all games"""
        games = Game.objects.all()
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """handles GET requests for individual game"""
        game = Game.objects.get(pk=pk)
        serialized = GameSerializer(game, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """handles POST requests for game view"""
        player_w = Player.objects.get(pk=request.data['player_w'])
        if request.data['player_b'] is not None:
            player_b = Player.objects.get(pk=request.data['player_b'])
        serialized = CreateGameSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        if request.data['player_b'] is not None:
            serialized.save(player_w=player_w, player_b=player_b)
        else:
            serialized.save(player_w=player_w)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """handles DELETE requests for game view"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """handles PUT requests for game view"""
        game = Game.objects.get(pk=pk)
        # winner = Player.objects.get(pk = request.data['winner'])
        # game.winner = winner.id
        game.winner_id = request.data['winner']
        if game.winner_id is not None:
            game.win_style = "checkmate"
        else:
            game.win_style = "draw"
        # game.w_notes = request.data['w_notes']
        # game.b_notes = request.data['b_notes']
        if game.pgn is not None:
            game.pgn = request.data['pgn']
        game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # @action(methods=['post'], detail=False)
    # def outcomes(self, request):
    #     """creates game objects in api from arr sent from client tournament module"""
    #     for outcome in request.data:
    #         player_w = Player.objects.get(pk=outcome['player_w'])
    #         player_b = Player.objects.get(pk=outcome['player_b'])
    #         if outcome['winner'] is not None:
    #             winner = Player.objects.get(pk=outcome['winner'])
    #         else:
    #             winner = None
    #         tournament = Tournament.objects.get(pk=outcome['tournament'])
    #         serialized = CreateGameSerializer(data=outcome)
    #         serialized.is_valid(raise_exception=True)
    #         serialized.save(player_w=player_w,
    #                         player_b=player_b,
    #                         tournament=tournament,
    #                         winner=winner)
    #     return Response(request.data, status=status.HTTP_201_CREATED)
    # @action(methods=['put'], detail=False)
    # def tournament_update(self, request):
    #     """updates previously created game objects from client tournament module"""
    #     for outcome in request.data:
    #         player_w = Player.objects.get(pk=outcome['player_w'])
    #         player_b = Player.objects.get(pk=outcome['player_b'])
    #         game = Game.objects.get(tournament_round = outcome['tournament_round'], tournament_id=outcome['tournament'], player_w=player_w, player_b=player_b)
    #         game.winner = outcome['winner']
    #         game.win_style = outcome['win_style']
    #         game.save()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)