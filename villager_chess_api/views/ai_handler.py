import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from rest_framework.viewsets import ViewSet
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.response import Response
from rest_framework import serializers, status


import os
import openai


api_key = os.getenv("CHESS_KEY")
openai.api_key = api_key

# class AiSerializer(serializers.Serializer):
#     class Meta:
#         fields = ('move')
class AiView(ViewSet):
    """coordinates responses to ai requests"""

    def create(self, request):
        # if self.path == "/ai":
        fen = request.data['fen']
        pgn = request.data['pgn']
        possible_moves = request.data['possibleMoves']
        color = request.data['color']
        # self._set_headers(201)

        instructions = [
            {"role": "system", "content": "You are a helpful assistant,"},
            # {"role": "user", "content": f"You are playing chess against the user as {color} and trying to win the game. The current PGN is {pgn}. The current FEN notation is {fen}. The valid moves available to you are {possible_moves}. Pick a move from the list that maximizes your chance of winning and provide an explanation for why you chose that option. Return your response in JSON object format with these properties: 'move' and 'explanation'. Pick a move even if you don't have a good option."}
            {"role": "user", "content": f"You are playing chess against the user as {color} and trying to win the game. The current PGN is {pgn}. The current FEN notation is {fen}. The valid moves available to you are {possible_moves}. Pick a move from the list that maximizes your chance of winning. Return your response in the same format as this example: 'move: e5'. Pick a move even if you don't have a good option and do not provide any data outside of the provided format."}

        ]

        move_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=instructions)

        response = move_completion.choices[0].message.content
        # serialized = AiSerializer(response)
        return Response(response, status=status.HTTP_201_CREATED)

#     def _set_headers(self, status):
#         """Sets the status code, Content-Type and Access-Control-Allow-Origin
#         headers on the response

#         Args:
#             status (number): the status code to return to the front end
#         """
#         self.send_response(status)
#         self.send_header('Content-type', 'application/json')
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.end_headers()

#     def do_OPTIONS(self):
#         """Sets the options headers
#         """
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods',
#                          'GET, POST, PUT, DELETE')
#         self.send_header('Access-Control-Allow-Headers',
#                          'X-Requested-With, Content-Type, Accept')

#         self.end_headers()

# def main():
#     """Starts the server on port 8088 using the HandleRequests class
#     """
#     host = ''
#     port = 8088
#     HTTPServer((host, port), AiView).serve_forever()


# if __name__ == "__main__":
#     main()
