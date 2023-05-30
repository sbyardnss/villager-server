from django.db import models


class Game(models.Model):
    """game model"""
    player_w = models.ManyToManyField(
        "Player", on_delete=models.CASCADE, related_name="games_as_white")
    player_b = models.ManyToManyField(
        "Player", on_delete=models.CASCADE, related_name="games_as_black")
    datetime = models.DateTimeField()
    w_notes = models.CharField()
    b_notes = models.CharField()
    tournament = models.ForeignKey(
        "Tournament", blank=True, null=True, on_delete=models.CASCADE, related_name="tournament")
    time_setting = models.ForeignKey('TimeSetting', on_delete=models.SET_NULL)
