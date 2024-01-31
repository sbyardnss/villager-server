from rest_framework import serializers
from villager_chess_api.models import ChessClub
from .player_serializers import PlayerRelatedSerializer
from .guest_player_serializers import GuestPlayerSerializer


class ChessClubSerializer(serializers.ModelSerializer):
    manager = PlayerRelatedSerializer(many=False)
    members = PlayerRelatedSerializer(many=True)
    guest_members = GuestPlayerSerializer(many=True)
    class Meta:
        model = ChessClub
        fields = ('id', 'name', 'manager', 'date',
                  'address', 'city', 'state', 'zipcode', 'details', 'members', 'guest_members', 'has_password')


class CreateChessClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ['id', 'name', 'address',
                  'city', 'state', 'zipcode', 'details', 'password']

class ClubRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChessClub
        fields = ('id', 'name')