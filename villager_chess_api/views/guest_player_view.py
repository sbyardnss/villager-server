from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from villager_chess_api.models import GuestPlayer

class GuestPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'name', 'guest_id')

class GuestView(ViewSet):
    """handles rest requests for guest users for tournament participation"""
    def list(self, pk=None):
        guests = GuestPlayer.objects.all()
        serialized = GuestPlayerSerializer(guests, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request):
        guest = GuestPlayer.objects.get(guest_id = request.data['guestId'])
        serialized = GuestPlayerSerializer(guest, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)