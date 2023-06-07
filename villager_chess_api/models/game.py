from django.db import models


class Game(models.Model):
    """game model"""
    player_w = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="games_as_white")
    player_b = models.ForeignKey(
        "Player", on_delete=models.CASCADE, related_name="games_as_black")
    date_time = models.DateTimeField(auto_now=True)
    w_notes = models.CharField(max_length=100, default="")
    b_notes = models.CharField(max_length=100, default="", null=True, blank=True)
    tournament = models.ForeignKey(
        "Tournament", blank=True, null=True, on_delete=models.CASCADE, related_name="games")
    tournament_round = models.IntegerField(default=1, null=True, blank=True)
    time_setting = models.ForeignKey(
        'TimeSetting', on_delete=models.SET_NULL, null=True, blank=True)
    pgn = models.CharField(max_length=400, null=True, blank=True)
    winner = models.ForeignKey(
        "Player", on_delete=models.SET_NULL, null=True, blank=True, related_name="wins")
    win_style = models.CharField(max_length=20, blank=True)
    accepted = models.BooleanField(default=False)

    @property
    def is_tournament(self):
        '''add boolean property to check if this game is part of a tournament'''
        return self.__is_tournament

    @is_tournament.setter
    def is_tournament(self, value):
        self.__is_tournament = value
