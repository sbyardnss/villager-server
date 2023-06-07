from django.db import models


class Tournament(models.Model):
    """tournament model"""
    title = models.CharField(max_length=50)
    creator = models.ForeignKey('Player', on_delete=models.SET_DEFAULT, default=1, related_name="my_tournaments")
    date = models.DateField(auto_now=True)
    competitors = models.ManyToManyField('Player', related_name='joined_tournaments')
    time_setting = models.ForeignKey(
        'TimeSetting', on_delete=models.DO_NOTHING, default=0,
        related_name="tournaments_with_time_setting")
    rounds = models.IntegerField(default=1)
    complete = models.BooleanField(default=False)
    # pairings = models.JSONField(default=list)
