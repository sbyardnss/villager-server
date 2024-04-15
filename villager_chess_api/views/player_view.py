from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count, Q
from villager_chess_api.models import Player, ChessClub
from villager_chess_api.serializers import PlayerSerializer, PlayerProfileSerializer, CreatePlayerSerializer, GuestPlayerSerializer, PlayerRelatedSerializer

class PlayerView(ViewSet):
    """handles rest requests for player objects"""

    def retrieve(self, request, pk=None):
        """handle request for individual player"""
        player = Player.objects.get(pk=pk)
        serialized = PlayerSerializer(player, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def list(self, request):
        """handle request for all players"""
        active_player = Player.objects.get(user=request.auth.user)
        players = Player.objects.annotate(is_friend=Count(
            'followers', filter=Q(followers=active_player)
        ))
        if "email" in request.query_params:
            players = players.filter(email=request.query_params['email'])
        serialized = PlayerSerializer(players, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """handle post requests to player view"""
        serialized = CreatePlayerSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """handles put requests for player view"""
        player = Player.objects.get(pk=pk)
        player.user.username = request.data['username']
        player.user.set_password(request.data['password'])
        player.user.email = request.data['email']
        player.user.first_name = request.data['first_name']
        player.user.last_name = request.data['last_name']
        player.user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def add_friend(self, request, pk):
        """add friend to player.friends"""
        player = Player.objects.get(user=request.auth.user)
        friend = Player.objects.get(pk=pk)
        player.friends.add(friend)
        return Response({'message': 'friend added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_friend(self, request, pk):
        """remove friend from player.friends"""
        player = Player.objects.get(user=request.auth.user)
        friend = Player.objects.get(pk=pk)
        player.friends.remove(friend)
        return Response({'message': 'friend removed'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def profile(self, request):
        """get sensitive player info for profile update"""
        player = Player.objects.get(user=request.auth.user)
        serialized = PlayerProfileSerializer(player, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    # THIS ACTION WORKED BUT WAS RETURNING DUPLICATE INFO
    # @action(methods=['get'], detail=False)
    # def club_mates(self, request):
    #     player = Player.objects.get(user=request.auth.user)
    #     clubs = ChessClub.objects.filter(members=player)
    #     players = []
    #     guests = []
    #     for club in clubs:
    #         # Add all players from the club to the list
    #         players.extend(club.members.all())
    #         # Add all guests from the club to the list
    #         guests.extend(club.guest_members.all())
    #     serialized_players = PlayerRelatedSerializer(players, many=True)
    #     serialized_guests = GuestPlayerSerializer(guests, many=True)
    #     serialized_all = serialized_players.data + serialized_guests.data
    #     return Response(serialized_all, status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False)
    def club_mates(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.filter(members=player)
        players = set()
        guests = set()
        for club in clubs:
            # Add all players from the club to the set, ensuring uniqueness
            players.update(club.members.all().distinct())
            # Add all guests from the club to the set, ensuring uniqueness
            guests.update(club.guest_members.all().distinct())
        # Convert sets back to lists for serialization
        serialized_players = PlayerRelatedSerializer(list(players), many=True)
        serialized_guests = GuestPlayerSerializer(list(guests), many=True)
        serialized_all = serialized_players.data + serialized_guests.data
        return Response(serialized_all, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False)
    def get_active_player(self, request):
      player = Player.objects.get(user=request.auth.user)
      serialized = PlayerRelatedSerializer(player, many=False)
      return Response(serialized.data, status=status.HTTP_200_OK)
      
