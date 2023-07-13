from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Player, GuestPlayer, Game, Tournament, TimeSetting, ChessClub
from django.contrib.contenttypes.models import ContentType


class PlayerOnClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')


class ChessClubSerializer(serializers.ModelSerializer):
    manager = PlayerOnClubSerializer(many=False)

    class Meta:
        model = ChessClub
        fields = ('id', 'name', 'manager', 'date',
                  'address', 'city', 'state', 'zipcode', 'details')


class CreateChessClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ['id', 'name', 'address',
                  'city', 'state', 'zipcode', 'details']


class ChessClubView(ViewSet):
    """handles rest requests for chess club objects"""

    def list(self, request):
        """handles GET requests for all clubs"""
        clubs = ChessClub.objects.all()
        serialized = ChessClubSerializer(clubs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """handles GET requests for single club"""
        club = ChessClub.objects.get(pk=pk)
        serialized = ChessClubSerializer(club, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        manager = Player.objects.get(user=request.auth.user)
        serialized = CreateChessClubSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(manager=manager)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        club.name = request.data['name']
        club.address = request.data['address']
        club.state = request.data['state']
        club.zipcode = request.data['zipcode']
        club.details = request.data['details']
        club.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        club.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
