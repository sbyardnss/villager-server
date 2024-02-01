import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from villager_chess_api.models import CommunityPost, Player, ChessClub

class CommunityPostViewTest(APITestCase):
    fixtures = ['users', 'tokens', 'community_posts', 'chess_clubs', 'players', 'guest_players']
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)

        self.club = ChessClub.objects.create(name='Test Club')
        self.post = CommunityPost.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    def test_list(self):
        # initial test for 1
        response = self.client.get('http://localhost:8000/communityposts') # replace '/communitypost/' with the actual URL
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 1)

        community_post = CommunityPost()
        community_post.poster = self.player
        community_post.date_time = "2023-05-12T21:19:25.057Z"
        community_post.message = "This is a test message"
        community_post.club = self.club
        community_post.save()

        response = self.client.get('http://localhost:8000/communityposts') # replace '/communitypost/' with the actual URL
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 2)
