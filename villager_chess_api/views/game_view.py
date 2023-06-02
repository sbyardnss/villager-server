from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Player, Game, Tournament


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
                  'is_tournament', 'time_setting', 'winner', 'pgn')
class CreateGameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['id', 'date_time', 'is_tournament', 'time_setting']


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
        player_w = Player.objects.get(pk=request.data['playerW'])
        player_b = Player.objects.get(pk=request.data['playerB'])
        serialized = CreateGameSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(player_w=player_w, player_b=player_b)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk=None):
        """handles DELETE requests for game view"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def update(self, request, pk=None):
        """handles PUT requests for game view"""
        game = Game.objects.get(pk=pk)
        game.winner = request.data['winner']
        game.win_style = request.data['winStyle']
        game.w_notes = request.data['wNotes']
        game.b_notes = request.data['bNotes']
        game.pgn = request.data['pgn']
        game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
