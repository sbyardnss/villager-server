from rest_framework.viewsets import ViewSet
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Player, Game, Tournament, ChessClub


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')


class PlayerProfileSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'full_name', 'first_name',
                  'last_name', 'email', 'username', 'friends')


class PlayerSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'full_name', 'email',
                  'username', 'friends', 'is_friend', 'my_clubs')


class CreatePlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'user')


class PlayerView(ViewSet):
    """handles rest requests for player objects"""

    def retrieve(self, request, pk=None):
        """handle request for individual player"""
        player = Player.objects.get(pk=pk)
        serialized = PlayerSerializer(player, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """handle request for all players"""
        active_player = Player.objects.get(user=request.auth.user)
        players = Player.objects.annotate(is_friend=Count(
            'followers', filter=Q(followers=active_player)
        ))
        if "email" in request.query_params:
            players = players.filter(email=request.query_params['email'])
        serialized = PlayerSerializer(players, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """handle post requests to player view"""
        serialized = CreatePlayerSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """handles put requests for player view"""
        player = Player.objects.get(pk=pk)
        player.user.username = request.data['username']
        player.user.set_password(request.data['password'])
        player.user.email = request.data['email']
        player.user.first_name = request.data['first_name']
        player.user.last_name = request.data['last_name']
        player.user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def add_friend(self, request, pk):
        """add friend to player.friends"""
        player = Player.objects.get(user=request.auth.user)
        friend = Player.objects.get(pk=pk)
        player.friends.add(friend)
        return Response({'message': 'friend added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_friend(self, request, pk):
        """remove friend from player.friends"""
        player = Player.objects.get(user=request.auth.user)
        friend = Player.objects.get(pk=pk)
        player.friends.remove(friend)
        return Response({'message': 'friend removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def profile(self, request):
        """get sensitive player info for profile update"""
        player = Player.objects.get(user=request.auth.user)
        serialized = PlayerProfileSerializer(player, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    
