from django.db import models


class Game(models.Model):
    """game model"""
    player_w = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="games_as_white")
    player_b = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="games_as_black")
    datetime = models.DateTimeField()
    w_notes = models.CharField(max_length=100, default="")
    b_notes = models.CharField(max_length=100, default="")
    tournament = models.ForeignKey(
        "Tournament", blank=True, null=True, on_delete=models.CASCADE, related_name="tournament")
    time_setting = models.ForeignKey('TimeSetting', on_delete=models.SET_NULL)
