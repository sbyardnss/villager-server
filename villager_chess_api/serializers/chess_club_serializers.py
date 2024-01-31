from rest_framework import serializers
from villager_chess_api.models import ChessClub
from .player_serializers import PlayerOnClubSerializer
from .guest_player_serializers import GuestOnClubSerializer


class ChessClubSerializer(serializers.ModelSerializer):
    manager = PlayerOnClubSerializer(many=False)
    members = PlayerOnClubSerializer(many=True)
    guest_members = GuestOnClubSerializer(many=True)
    class Meta:
        model = ChessClub
        fields = ('id', 'name', 'manager', 'date',
                  'address', 'city', 'state', 'zipcode', 'details', 'members', 'guest_members', 'has_password')


class CreateChessClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ['id', 'name', 'address',
                  'city', 'state', 'zipcode', 'details', 'password']

