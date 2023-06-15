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
                  'is_tournament', 'time_setting', 'winner', 'pgn', 'bye', 'accepted')


class CreateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['id', 'date_time', 'time_setting', 'tournament', 'win_style', 'winner', 'accepted', 'tournament_round', 'bye', 'pgn', 'computer_opponent']


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
        if request.data['player_w'] is not None:
            player_w = Player.objects.get(pk=request.data['player_w'])
        if request.data['player_b'] is not None:
            player_b = Player.objects.get(pk=request.data['player_b'])
        serialized = CreateGameSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        if request.data['player_w'] is not None:
            serialized.save(player_w=player_w)
        if request.data['player_b'] is not None:
            serialized.save(player_b=player_b)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """handles DELETE requests for game view"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """handles PUT requests for game view"""
        game = Game.objects.get(pk=pk)
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
    @action(methods=['put'], detail=True)
    def accept_challenge(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        game.player_w = Player.objects.get(pk= request.data['player_w'])
        game.player_b = Player.objects.get(pk= request.data['player_b'])
        game.accepted = request.data['accepted']
        game.save()
        return Response({"message": "challenge accepted"}, status=status.HTTP_204_NO_CONTENT)
