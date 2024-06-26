from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from villager_chess_api.models import CommunityPost
from villager_chess_api.serializers import CreateCommunityPostSerializer, CommunityPostSerializer
from rest_framework.decorators import action

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

    @action(methods=['post'], detail=False)
    def get_my_clubs_posts(self, request, pk=None):
        community_posts=CommunityPost.objects.filter(club__in=request.data)
        serialized = CommunityPostSerializer(community_posts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
