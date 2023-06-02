from django.db import models


class Tournament(models.Model):
    """tournament model"""
    title = models.CharField(max_length=50)
    creator = models.ForeignKey('Player', on_delete=models.SET_DEFAULT, default=1, related_name="my_tournaments")
    date = models.DateField()
    time_setting = models.ForeignKey(
        'TimeSetting', on_delete=models.DO_NOTHING, default=0,
        related_name="tournaments_with_time_setting")
    complete = models.BooleanField(default=False)
