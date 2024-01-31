from villager_chess_api.models import Player
from rest_framework import serializers

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')

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

class PlayerOnClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')


class PlayerProfileSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True)

    class Meta:
        model = Player
        fields = ('id', 'user', 'full_name', 'first_name',
                  'last_name', 'email', 'username', 'friends')

class CommunityPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name', 'username')