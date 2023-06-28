from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from villager_chess_api.models import GuestPlayer

class GuestPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'name', 'guest_id')

class CreateGuestPlayerSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = ['id', 'name']
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
    def create(self, request):
        serialized = CreateGuestPlayerSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk=None):
        guest = GuestPlayer.objects.get(pk=pk)
        guest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)