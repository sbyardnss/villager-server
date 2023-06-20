import json
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import time

import os
import openai
from openai.error import ServiceUnavailableError


api_key = os.getenv("CHESS_KEY")
openai.api_key = api_key

# class AiSerializer(serializers.Serializer):
#     class Meta:
#         fields = ('move')


class AiView(ViewSet):
    """coordinates responses to ai requests"""

    def create(self, request):
        fen = request.data['fen']
        pgn = request.data['pgn']
        possible_moves = request.data['possibleMoves']
        color = request.data['color']
        instructions = [
            {"role": "system", "content": "You are a very skilled chess player who always thinks about their available valid moves before choosing one. You only respond in the format: move: e5"},
            # {"role": "user", "content": f"You are playing chess against the user as {color} and trying to win the game. The current PGN is {pgn}. The current FEN notation is {fen}. The valid moves available to you are {possible_moves}. Pick a move from the list that maximizes your chance of winning. Return your response in the same format as this example: 'move: e5'. Pick a move even if you don't have a good option and do not provide any data outside of the provided format."}
            {"role": "user", "content": f"You are playing chess against the user as {color} and trying to win the game. The current PGN is {pgn}. The current FEN notation is {fen}. You MUST pick from one of the available moves listed in {possible_moves}. Pick a move from the list that maximizes your chance of winning. Return your response in the same format as this example: 'move: e5'. Pick a move even if you don't have a good option and do not provide any data outside of the provided format."}
        ]
        # try:
        move_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=instructions)
        response = move_completion.choices[0].message.content
        return Response(response, status=status.HTTP_201_CREATED)
        # except ServiceUnavailableError as e:
        #     time.sleep(5)
            

