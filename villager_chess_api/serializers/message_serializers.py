from rest_framework import serializers
from villager_chess_api.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'message', 'date_time', 'sender', 'recipient', 'read')


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'recipient', 'message', 'date_time']
