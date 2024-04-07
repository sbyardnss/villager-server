from rest_framework import serializers
from villager_chess_api.models import Game, GuestPlayer, Player
from .guest_player_serializers import GuestPlayerSerializer
from .player_serializers import PlayerRelatedSerializer
from django.contrib.contenttypes.models import ContentType

class PlayerObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """
    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, GuestPlayer):
            serializer = GuestPlayerSerializer(value, many=False)
        elif isinstance(value, Player):
            serializer = PlayerRelatedSerializer(value, many=False)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data

# WE DONT NEED CT FOR PLAYERS IN FRONTEND TARGET_WINNER_CT, ETC
class GameSerializer(serializers.ModelSerializer):
    player_w = PlayerObjectRelatedField(many=False, read_only=True)
    player_b = PlayerObjectRelatedField(many=False, read_only=True)
    winner = PlayerObjectRelatedField(many=False, read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'player_w', 'player_b', 'date_time', 'tournament', 'tournament_round',
                  'time_setting', 'winner', 'pgn', 'bye', 'accepted', 'win_style', 'target_winner_ct', 'target_player_b_ct', 'target_player_w_ct')  # removed target_winner_ct, target_player_b_ct, target_player_w_ct


class CreateGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'date_time', 'time_setting', 'tournament', 'win_style',
                  'accepted', 'tournament_round', 'bye', 'pgn', 'computer_opponent']
# this line gets
# print(ContentType.objects.get_for_model(GuestPlayer).model)

print(ContentType.objects.get_for_model(Player))
