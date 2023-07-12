from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Player, GuestPlayer, Game, Tournament, TimeSetting
from django.contrib.contenttypes.models import ContentType


class PlayerOnGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')


class GuestOnGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'full_name', 'guest_id')


class PlayerObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, GuestPlayer):
            serializer = GuestOnGameSerializer(value, many=False)
        elif isinstance(value, Player):
            serializer = PlayerOnGameSerializer(value, many=False)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data
# PRE GFK FIELD SERIALIZER
# class GameSerializer(serializers.ModelSerializer):
#     player_w = PlayerOnGameSerializer(many=False)
#     player_b = PlayerOnGameSerializer(many=False)
#     winner = PlayerOnGameSerializer(many=False)

#     class Meta:
#         model = Game
#         fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
#                   'is_tournament', 'time_setting', 'winner', 'pgn', 'bye', 'accepted', 'win_style')


class GameSerializer(serializers.ModelSerializer):
    player_w = PlayerObjectRelatedField(many=False, read_only=True)
    player_b = PlayerObjectRelatedField(many=False, read_only=True)
    winner = PlayerObjectRelatedField(many=False, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
                  'is_tournament', 'time_setting', 'winner', 'pgn', 'bye', 'accepted', 'win_style', 'target_winner_ct', 'target_player_b_ct', 'target_player_w_ct')  # removed target_winner_ct, target_player_b_ct, target_player_w_ct


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'date_time', 'time_setting', 'tournament', 'win_style',
                  'accepted', 'tournament_round', 'bye', 'pgn', 'computer_opponent']
# this line gets
# print(ContentType.objects.get_for_model(GuestPlayer).model)


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
        # print(request.data)
        """handles POST requests for game view"""
        # if request.data['player_w'] is not None:
        #     player_w = Player.objects.get(pk=request.data['player_w'])
        # if request.data['player_b'] is not None:
        #     player_b = Player.objects.get(pk=request.data['player_b'])
        if request.data['player_w'] is not None:
            if request.data['player_w_model_type'] == 'guestplayer':
                numeric_guest_id = int(request.data['player_w'].split('g')[1])
                target_player_w_id = GuestPlayer.objects.get(
                    pk=numeric_guest_id).id
                target_player_w_ct = ContentType.objects.get_for_model(
                    GuestPlayer)
            else:
                target_player_w_id = Player.objects.get(
                    pk=request.data['player_w']).id
                target_player_w_ct = ContentType.objects.get_for_model(
                    Player)
                # print(f'{target_player_w_ct} {target_player_w_id}')
        if request.data['player_b'] is not None:
            if request.data['player_b_model_type'] == 'guestplayer':
                numeric_guest_id = int(request.data['player_b'].split('g')[1])
                target_player_b_id = GuestPlayer.objects.get(
                    pk=numeric_guest_id).id
                target_player_b_ct = ContentType.objects.get_for_model(
                    GuestPlayer)
                # print(f'{target_player_b_ct} {target_player_b_id}')
            else:
                target_player_b_id = Player.objects.get(
                    pk=request.data['player_b']).id
                target_player_b_ct = ContentType.objects.get_for_model(
                    Player)
        if request.data['winner'] is not None:
            if request.data['winner_model_type'] == 'guestplayer':
                numeric_guest_id = int(request.data['winner'].split('g')[1])
                target_winner_id = GuestPlayer.objects.get(
                    pk=numeric_guest_id).id
                target_winner_ct = ContentType.objects.get_for_model(
                    GuestPlayer)
            else:
                target_winner_id = Player.objects.get(
                    pk=request.data['winner']).id
                target_winner_ct = ContentType.objects.get_for_model(Player)
        serialized = CreateGameSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        if request.data['player_w'] is not None:
            serialized.save(target_player_w_id=target_player_w_id,
                            target_player_w_ct=target_player_w_ct)
        else:
            serialized.save(target_player_w_id=None,
                            target_player_w_ct=None)
        if request.data['player_b'] is not None:
            serialized.save(target_player_b_id=target_player_b_id,
                            target_player_b_ct=target_player_b_ct)
        else:
            serialized.save(target_player_b_id=None,
                            target_player_b_ct=None)
        if request.data['winner'] is not None:
            serialized.save(target_winner_id=target_winner_id,
                            target_winner_ct=target_winner_ct)
        else:
            serialized.save(target_winner_id=None,
                            target_winner_ct=None)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        """handles DELETE requests for game view"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """handles PUT requests for game view"""
        # game = Game.objects.get(pk=pk)
        # game.winner_id = request.data['winner']
        # if game.winner_id is not None:
        #     game.win_style = "checkmate"
        # else:
        #     game.win_style = "draw"
        # # game.w_notes = request.data['w_notes']
        # # game.b_notes = request.data['b_notes']
        # if request.data['pgn'] is not None:
        #     game.pgn = request.data['pgn']
        # game.save()
        # return Response(None, status=status.HTTP_204_NO_CONTENT)
        game = Game.objects.get(pk=pk)
        # print(game.target_winner_ct)
        if request.data['winner'] is not None:
            if request.data['winner_model_type'] == 'guestplayer':
                numeric_guest_id = int(request.data['winner'].split('g')[1])
                target_winner_id = GuestPlayer.objects.get(
                    pk=numeric_guest_id).id
                target_winner_ct = ContentType.objects.get_for_model(
                    GuestPlayer)
                game.target_winner_id = target_winner_id
                game.target_winner_ct = target_winner_ct
                game.save()
            elif request.data['winner'] is None and request.data['win_style'] == 'draw':
                game.win_style = request.data['win_style']
                game.target_winner_ct = None
                game.target_winner_id = None
                game.save()
            else:
                target_winner_id = Player.objects.get(
                    pk=request.data['winner']).id
                target_winner_ct = ContentType.objects.get_for_model(Player)
                game.target_winner_ct = target_winner_ct
                game.target_winner_id = target_winner_id
                game.save()
        if request.data['pgn'] is not None:
            game.pgn = request.data['pgn']
            game.save()
        # game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def accept_challenge(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        game.player_w = Player.objects.get(pk=request.data['player_w'])
        game.player_b = Player.objects.get(pk=request.data['player_b'])
        game.accepted = request.data['accepted']
        game.save()
        return Response({"message": "challenge accepted"}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def my_games(self, request):
        player = Player.objects.get(user=request.auth.user)
        games = Game.objects.filter(
            Q(player_w__id=player.id) | Q(player_b__id=player.id))
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_selected_tournament_games(self, request, pk=None):
        games = Game.objects.filter(tournament=pk)
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
