from django.db import models
# added two below to allow multiple models on one foreign key field
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# for c in ContentType.objects.filter(model = 'guestplayer'):
#     print(c.pk)
class Game(models.Model):
    """game model"""
    # beginning of multiple models on fk field code
    limit = models.Q(model='Player') | models.Q(model='GuestPlayer')
    target_player_w_id = models.PositiveIntegerField(null=True)
    target_player_w_ct = models.ForeignKey(
        ContentType, limit_choices_to=limit, null=True, related_name="player_w", on_delete=models.CASCADE)
    player_w = GenericForeignKey("target_player_w_ct", "target_player_w_id")

    target_player_b_id = models.PositiveIntegerField(null=True)
    target_player_b_ct = models.ForeignKey(
        ContentType, limit_choices_to=limit, null=True, related_name="player_b", on_delete=models.CASCADE)
    player_b = GenericForeignKey("target_player_b_ct", "target_player_b_id")

    target_winner_id = models.PositiveIntegerField(null=True)
    target_winner_ct = models.ForeignKey(
        ContentType, limit_choices_to=limit, null=True, blank=True, related_name="winner", on_delete=models.CASCADE)
    winner = GenericForeignKey("target_winner_ct", "target_winner_id")
    # end of multiple models on fk field

    date_time = models.DateTimeField(auto_now=True)
    # w_notes = models.CharField(max_length=100, default="")
    # b_notes = models.CharField(max_length=100, default="", null=True, blank=True)
    tournament = models.ForeignKey(
        "Tournament", blank=True, null=True, on_delete=models.CASCADE, related_name="games")
    tournament_round = models.IntegerField(default=1, null=True, blank=True)
    time_setting = models.ForeignKey(
        'TimeSetting', on_delete=models.SET_NULL, null=True, blank=True)
    pgn = models.CharField(max_length=400, null=True, blank=True)
    win_style = models.CharField(max_length=20, blank=True)
    accepted = models.BooleanField(default=False)
    bye = models.BooleanField(default=False)
    computer_opponent = models.BooleanField(default=False)
    # turn = models.CharField(default="w", null=True)
    
    @property
    def is_tournament(self):
        '''add boolean property to check if this game is part of a tournament'''
        return self.__is_tournament

    @is_tournament.setter
    def is_tournament(self, value):
        self.__is_tournament = value


