from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from villager_chess_api.models import Player

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a player
    
    Method arguments:
    request -- The full HTTP request object
    '''
    print(request.data)
    username = request.data['username']
    password = request.data['password']
    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)
    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        player = Player.objects.get(user = authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'userId': player.id
        }
        return Response(data, status=status.HTTP_200_OK)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new player for authentication
    
    Method arguments:
    request -- The full HTTP request object
    '''
    
    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )
    already_registered = Player.objects.get(user__email=new_user.email)
    if already_registered is not None:
        data = {
            "message": "email already in use"
        }
    else:
        # Now save the extra info in the levelupapi_gamer table
        player = Player.objects.create(
            user=new_user
        )
        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=player.user)
        # Return the token to the client
        data = {
            'valid': True,
            'token': token.key,
            'userId': player.id
        }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def check_player_registered(self, request):
    """get player by email for check prior to register"""
    email= self.data['email']
    authenticated_user = authenticate(email=email)
    if authenticated_user is not None:
        return Response({"message": "email in use"}, status=status.HTTP_200_OK)
    else:
        print("none")
        return Response(None, status=status.HTTP_404_NOT_FOUND)
    # try:
    #     player = Player.objects.get(
    #         user__email=request.query_params['email'])
    #     serialized = PlayerProfileSerializer(player, many=False)
    #     return Response(serialized.data, status=status.HTTP_200_OK)
    # except Player.DoesNotExist as ex:
    #     return Response(None, status=status.HTTP_404_NOT_FOUND)
