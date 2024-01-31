from rest_framework import serializers
from villager_chess_api.models import CommunityPost
from .player_serializers import CommunityPosterSerializer



class CommunityPostSerializer(serializers.ModelSerializer):
    poster = CommunityPosterSerializer(many=False)
    class Meta:
        model = CommunityPost
        fields = ('id', 'poster', 'message', 'date_time', 'club')
class CreateCommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = ['id', 'poster', 'message', 'date_time', 'club']
