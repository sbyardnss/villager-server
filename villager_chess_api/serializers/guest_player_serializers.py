from villager_chess_api.models import GuestPlayer
from rest_framework import serializers

class GuestOnClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'full_name', 'guest_id')