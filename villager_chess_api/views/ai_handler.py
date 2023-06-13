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


class AiView(ViewSet):
    """coordinates responses to ai requests"""

    def create(self, request):
        # if self.path == "/ai":

            # self._set_headers(201)


        instructions = [
            {"role": "system", "content": "you are a professional chess player. Based on the pgn provided what should the next move be? Respond only in the 'short algebraic notation' format. Nothing more."},
            {"role": "user", "content": f"{request.data['pgn']}"}
        ]
        move_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=instructions)
        response = move_completion.choices[0].message.content
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
