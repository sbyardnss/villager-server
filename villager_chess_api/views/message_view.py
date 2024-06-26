from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from villager_chess_api.models import Message, Player
from villager_chess_api.serializers import MessageSerializer, CreateMessageSerializer

class MessageView(ViewSet):
    """handle rest requests for message objects"""

    def list(self, request):
        """handles GET requests for all messages"""
        active_player = Player.objects.get(user=request.auth.user)
        messages = Message.objects.filter(
            Q(sender=active_player.id) | Q(recipient=active_player.id))
        serialized = MessageSerializer(messages, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """handles POST requests for message view"""
        player = Player.objects.get(user=request.auth.user)
        message = CreateMessageSerializer(data=request.data)
        message.is_valid(raise_exception=True)
        message.save(sender=player, read=False)
        return Response(message.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """handles PUT requests for message view"""
        message = Message.objects.get(pk=pk)
        message.read = request.data['read']
        message.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def unread(self, request):
        active_player = Player.objects.get(user=request.auth.user)
        messages = Message.objects.filter(read=0, recipient=active_player.id)
        serialized = MessageSerializer(messages, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
