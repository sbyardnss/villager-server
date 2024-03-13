from rest_framework import serializers
from villager_chess_api.models import Tournament
from .player_serializers import PlayerOnTournamentSerializer
from .guest_player_serializers import GuestPlayerSerializer
from .chess_club_serializers import ClubRelatedSerializer

class TournamentSerializer(serializers.ModelSerializer):
    creator = PlayerOnTournamentSerializer(many=False)
    # games = GameTournamentSerializer(many=True)
    competitors = PlayerOnTournamentSerializer(many=True)
    guest_competitors = GuestPlayerSerializer(many=True)
    # club = ClubRelatedSerializer(many=False)

    class Meta:
        model = Tournament
        fields = ('id', 'title', 'creator', 'games', 'time_setting',
                  'complete', 'competitors', 'guest_competitors', 'rounds', 'pairings', 'in_person', 'club', 'date')

class CreateTournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'title', 'time_setting', 'pairings', 'in_person', 'club']

