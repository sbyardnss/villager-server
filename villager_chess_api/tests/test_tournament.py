import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from villager_chess_api.models import CommunityPost, Player, ChessClub

class TournamentViewTest(APITestCase):
    fixtures = ['users', 'tokens', 'community_posts', 'chess_clubs', 'players', 'guest_players', 'tournaments', 'games', 'time_settings']
    def setUp(self):
        self.player = Player.objects.first()
        token = Token.objects.get(user=self.player.user)

        self.club = ChessClub.objects.create(name='Test Club')
        self.post = CommunityPost.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    def test_list(self):
        # initial test for 1
        response = self.client.get('http://localhost:8000/tournaments') # replace '/communitypost/' with the actual URL
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 1)

    # def test_retrieve(self):
    #     response = self.client.get(f'/communityposts/{self.post.id}/') # replace '/communitypost/' with the actual URL
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_create(self):
    #     response = self.client.post('/communityposts/', {'message': 'New message'}) # replace '/communitypost/' with the actual URL
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_update(self):
    #     response = self.client.put(f'/communityposts/{self.post.id}/', {'message': 'Updated message'}) # replace '/communitypost/' with the actual URL
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_destroy(self):
    #     response = self.client.delete(f'/communityposts/{self.post.id}/') # replace '/communitypost/' with the actual URL
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)