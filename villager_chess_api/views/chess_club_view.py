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
    members = PlayerOnClubSerializer(many=True)
    class Meta:
        model = ChessClub
        fields = ('id', 'name', 'manager', 'date',
                  'address', 'city', 'state', 'zipcode', 'details', 'members', 'guest_members')


class CreateChessClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ['id', 'name', 'address',
                  'city', 'state', 'zipcode', 'details', 'password']


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
        serialized.save(manager=manager, guest_members = [], members = [manager])
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        try:
            if request.data['oldPassword'] == club.password:
                club.name = request.data['name']
                club.address = request.data['address']
                club.state = request.data['state']
                club.zipcode = request.data['zipcode']
                club.details = request.data['details']
                club.password = request.data['newPassword']
                club.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValueError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        club.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def my_clubs(self, request):
        player = Player.objects.get(user = request.auth.user)
        clubs = ChessClub.objects.filter(members = player)
        serialized = ChessClubSerializer(clubs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
