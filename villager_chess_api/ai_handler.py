# import json
# from http.server import BaseHTTPRequestHandler, HTTPServer
# from urllib.parse import urlparse
# from rest_framework.viewsets import ViewSet
# import os
# import openai


# api_key = os.getenv("CHESS_KEY")
# openai.api_key = api_key
# class HandleAIRequests(ViewSet):
#     """coordinates responses to ai requests"""
#     def generate_move(self, request):