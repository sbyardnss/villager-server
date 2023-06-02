from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Count, Q
from django.contrib.auth.models import User
from villager_chess_api.models import Message, Tournament, Game, Player, TimeSetting


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'date_time', 'sender', 'recipient', 'read')


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'message', 'date_time', 'read']


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
        player = Player.objects.get(user=request.auth.user)
        # message = {
        #     'sender': player.id,
        #     'recipient': request.data['recipient'],
        #     'message': request.data['message'],
        #     'read': False
        #     # 'date_time': request.data['date_time']
        # }
        message = CreateMessageSerializer(data=request.data)
        message.is_valid(raise_exception=True)
        message.save(sender=player)
        return Response(message.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
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
