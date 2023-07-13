from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from villager_chess_api.models import GuestPlayer
from rest_framework.decorators import action


class GuestPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestPlayer
        fields = ('id', 'full_name', 'guest_id')

class CreateGuestPlayerSerializer(serializers.ModelSerializer):
    class Meta: 
        fields = ['id', 'full_name']
class GuestView(ViewSet):
    """handles rest requests for guest users for tournament participation"""
    def list(self, pk=None):
        guests = GuestPlayer.objects.all()
        serialized = GuestPlayerSerializer(guests, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        guest_id = pk
        numeric_id = guest_id.split("g")[1]
        guest = GuestPlayer.objects.get(pk = numeric_id)
        serialized = GuestPlayerSerializer(guest, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    def create(self, request):
        serialized = CreateGuestPlayerSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    def destroy(self, request, pk=None):
        guest = GuestPlayer.objects.get(guest_id = request.data['guestId'])
        guest.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    # @action(methods=['post'], detail=True)
    # def test_get_guest_id(self, request, pk=None):
    #     # print(request.data)
    #     guest = GuestPlayer.objects.get(_guest_id = request.data['guestId'])
    #     serialized = GuestPlayerSerializer(guest, many=False)
    #     return Response(serialized.data, status=status.HTTP_200_OK)