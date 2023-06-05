from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
# from rest_framework.decorators import action
# from datetime import datetime
# from django.db.models import Count, Q
# from django.contrib.auth.models import User
from villager_chess_api.models import Player, CommunityPost

class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'full_name')

class CommunityPostSerializer(serializers.ModelSerializer):
    poster = PosterSerializer(many=False)
    class Meta:
        model = CommunityPost
        fields = ('id', 'poster', 'message', 'date_time')
class CreateCommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = ['id', 'poster', 'message', 'date_time']
class CommunityPostView(ViewSet):
    """handles rest requests for community post objects"""
    def list(self, request):
        """handles GET requests for all community posts"""
        posts = CommunityPost.objects.all()
        serialized = CommunityPostSerializer(posts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        """handles GET requests for single community post"""
        post = CommunityPost.objects.get(pk=pk)
        serialized = CommunityPostSerializer(post, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        """handles POST requests to community post view"""
        serialized = CreateCommunityPostSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def update(self, request, pk=None):
        """handles PUT requests for community post view"""
        post = CommunityPost.objects.get(pk=pk)
        post.message = request.data['message']
        post.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk=None):
        """handles DELETE requests to community post view"""
        post = CommunityPost.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

