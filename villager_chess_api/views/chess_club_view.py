from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from villager_chess_api.models import Player, ChessClub
from villager_chess_api.serializers import ChessClubSerializer, CreateChessClubSerializer

class ChessClubView(ViewSet):
    """handles rest requests for chess club objects"""

    def list(self, request):
        """handles GET requests for all clubs"""
        clubs = ChessClub.objects.all()
        serialized = ChessClubSerializer(clubs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """handles GET requests for single club"""
        club = ChessClub.objects.get(pk=pk)
        serialized = ChessClubSerializer(club, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        manager = Player.objects.get(user=request.auth.user)
        serialized = CreateChessClubSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)
        serialized.save(manager=manager, guest_members=[], members=[manager])
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        try:
            if request.data['old_password'] == club.password or club.password == None:
                # club.name = request.data['clubObj']['name']
                # club.address = request.data['clubObj']['address']
                # club.state = request.data['clubObj']['state']
                # club.zipcode = request.data['clubObj']['zipcode']
                # club.details = request.data['clubObj']['details']
                # club.password = request.data['clubObj']['newPassword']
                club.__dict__.update(request.data['clubObj'])
                if request.data['clubObj']['newPassword']:
                    club.password = request.data['clubObj']['newPassword']
                club.save()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValueError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        club.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def my_clubs(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.filter(members=player)
        serialized = ChessClubSerializer(clubs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False)
    def clubs_user_has_not_joined(self, request):
        player = Player.objects.get(user=request.auth.user)
        clubs = ChessClub.objects.exclude(members=player)
        serialized = ChessClubSerializer(clubs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def join_club(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        player = Player.objects.get(user=request.auth.user)
        if club.password is not None:
            if club.password == request.data['submittedPassword']:
                club.members.add(player)
                return Response({'message': 'club joined'}, status=status.HTTP_201_CREATED)
            if club.password != request.data['submittedPassword']:
                return Response({'message': 'incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            club.members.add(player)
            return Response({'message': 'club joined'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave_club(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        player = Player.objects.get(user=request.auth.user)
        club.members.remove(player)
        return Response({'message': 'club left'}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['delete'], detail=True)
    def end_club(self, request, pk=None):
        club = ChessClub.objects.get(pk=pk)
        player = Player.objects.get(user=request.auth.user)
        if (club.manager == player):
            club.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'not the creator'}, status=status.HTTP_401_UNAUTHORIZED)
    
    @action(methods=['put'], detail=True)
    def remove_club_password(self, request, pk=None):
        club=ChessClub.objects.get(pk=pk)
        try:
            if club.password ==request.data['password']:
                club.password = None
                club.save()
                return Response({'message': 'password removed'}, status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except AssertionError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)