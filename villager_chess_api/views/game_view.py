from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from villager_chess_api.models import Player, GuestPlayer, Game
from villager_chess_api.serializers import GameSerializer, CreateGameSerializer
from django.contrib.contenttypes.models import ContentType
import json
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

    def get_player_info(self, player_data, model_type):
        if player_data and 'id' in player_data:
            if model_type == 'guestplayer':
                player_model = GuestPlayer
                content_type = ContentType.objects.get_for_model(GuestPlayer)
            else:
                player_model = Player
                content_type = ContentType.objects.get_for_model(Player)
            player = player_model.objects.get(pk=player_data['id'])
            return player.id, content_type
        return None, None

    def create(self, request):
        """handles POST requests for game view"""
        # print(json.dumps(request.data, indent=4))
        
        target_player_w_id, target_player_w_ct = self.get_player_info(request.data.get('player_w'), request.data.get('player_w_model_type'))
        target_player_b_id, target_player_b_ct = self.get_player_info(request.data.get('player_b'), request.data.get('player_b_model_type'))
        target_winner_id, target_winner_ct = self.get_player_info(request.data.get('winner'), request.data.get('winner_model_type'))
        
        serialized = CreateGameSerializer(data=request.data, many=False)
        serialized.is_valid(raise_exception=True)
        # print(json.dumps(serialized.data))
        
        serialized.save(
            target_player_w_id=target_player_w_id,
            target_player_w_ct=target_player_w_ct,
            target_player_b_id=target_player_b_id,
            target_player_b_ct=target_player_b_ct,
            target_winner_id=target_winner_id,
            target_winner_ct=target_winner_ct
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    # def create(self, request):
    #     """handles POST requests for game view"""
    #     print(json.dumps(request.data, indent=4))
    #     if request.data['player_w'] is not None:
    #         player_w_data = request.data['player_w']
    #         if player_w_data is not None and 'id' in player_w_data:
    #             if request.data['player_w_model_type'] == 'guestplayer':
    #                 target_player_w = GuestPlayer.objects.get(pk=player_w_data['id'])
    #                 print(target_player_w)
    #                 target_player_w_id = target_player_w.id
    #                 target_player_w_ct = ContentType.objects.get_for_model(GuestPlayer)
    #             else:
    #                 target_player_w_id = Player.objects.get(pk=player_w_data['id']).id
    #                 target_player_w_ct = ContentType.objects.get_for_model(Player)
    #     if request.data['player_b'] is not None:
    #         player_b_data = request.data['player_b']
    #         print(json.dumps(player_b_data, indent=4))
    #         if player_b_data is not None and 'id' in player_b_data:
    #             if request.data['player_b_model_type'] == 'guestplayer':
    #                 target_player_b_id = GuestPlayer.objects.get(pk=player_b_data['id']).id
    #                 target_player_b_ct = ContentType.objects.get_for_model(GuestPlayer)
    #             else:
    #                 target_player_b = Player.objects.get(pk=player_b_data['id'])
    #                 print(target_player_b)
    #                 target_player_b_id = target_player_b.id
    #                 target_player_b_ct = ContentType.objects.get_for_model(
    #                     Player)
    #     if request.data['winner'] is not None:
    #         winner_data = request.data['winner']
    #         if winner_data is not None and 'id' in winner_data:
    #             if request.data['winner_model_type'] == 'guestplayer':
    #                 target_winner_id = GuestPlayer.objects.get(pk=winner_data['id']).id
    #                 target_winner_ct = ContentType.objects.get_for_model(GuestPlayer)
    #             else:
    #                 target_winner_id = Player.objects.get(pk=winner_data['id']).id
    #                 target_winner_ct = ContentType.objects.get_for_model(Player)
    #     serialized = CreateGameSerializer(data=request.data, many=False)
    #     serialized.is_valid(raise_exception=True)
    #     print(json.dumps(serialized.data))
    #     if request.data['player_w'] is not None:
    #         serialized.save(target_player_w_id=target_player_w_id,
    #                         target_player_w_ct=target_player_w_ct)
    #     else:
    #         serialized.save(target_player_w_id=None,
    #                         target_player_w_ct=None)
    #     if request.data['player_b'] is not None:
    #         serialized.save(target_player_b_id=target_player_b_id,
    #                         target_player_b_ct=target_player_b_ct)
    #     else:
    #         serialized.save(target_player_b_id=None,
    #                         target_player_b_ct=None)
    #     if request.data['winner'] is not None:
    #         serialized.save(target_winner_id=target_winner_id,
    #                         target_winner_ct=target_winner_ct)
    #     else:
    #         serialized.save(target_winner_id=None,
    #                         target_winner_ct=None)
    #     return Response(serialized.data, status=status.HTTP_201_CREATED)




    def destroy(self, request, pk=None):
        """handles DELETE requests for game view"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """handles PUT requests for game view"""
        game = Game.objects.get(pk=pk)
        # print(request.data)
        if request.data['winner'] is not None:
            if request.data['win_style'] == 'checkmate':
                game.win_style = 'checkmate'
            if request.data['winner_model_type'] == 'guestplayer':
                # numeric_guest_id = int(request.data['winner'].split('g')[1])
                # target_winner_id = GuestPlayer.objects.get(
                #     pk=numeric_guest_id).id
                # target_winner_ct = ContentType.objects.get_for_model(
                #     GuestPlayer)
                target_winner_id = GuestPlayer.objects.get(pk=request.data['winner']['id']).id
                target_winner_ct = ContentType.objects.get_for_model(GuestPlayer)
                game.target_winner_id = target_winner_id
                game.target_winner_ct = target_winner_ct
                game.save()
            else:
                target_winner_id = Player.objects.get(
                    pk=request.data['winner']['id']).id
                target_winner_ct = ContentType.objects.get_for_model(Player)
                game.target_winner_ct = target_winner_ct
                game.target_winner_id = target_winner_id
                game.save()
        else:
                game.win_style = request.data['win_style']
                game.target_winner_ct = None
                game.target_winner_id = None
                game.save()
        if request.data['pgn'] is not None:
            game.pgn = request.data['pgn']
            game.save()
        # game.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    @action(methods=['get'], detail=False)
    def get_active_user_games(self, request, pk=None):
        user = Player.objects.get(user=request.auth.user)
        active_user_games = Game.objects.filter(
            Q(target_player_w_id=user.id, target_player_w_ct=11) |
            Q(target_player_b_id=user.id, target_player_b_ct=11),
            Q(target_winner_id=None, target_winner_ct=None),
        )
        active_user_games = active_user_games.exclude(Q(win_style='draw') | Q(accepted = False))
        serialized = GameSerializer(active_user_games, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def get_open_challenges(self, request, pk=None):
        open_games = Game.objects.filter(accepted = False)
        serialized = GameSerializer(open_games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
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
            Q(target_player_w_ct_id = 11) & Q(target_player_w_id = player.id) | Q(target_player_b_ct_id = 11) & Q(target_player_b_id = player.id))
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_selected_tournament_games(self, request, pk=None):
        games = Game.objects.filter(tournament=pk)
        serialized = GameSerializer(games, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
