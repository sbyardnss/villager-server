from django.db import models

class TimeSetting(models.Model):
    """time setting model"""
    # time_choices = [
    #     (5, "five minutes"),
    #     (10, "ten minutes")
    # ]
    # time_clock = models.IntegerChoices(time_choices, default=5)
    # increment_choices = [
    #     (0, "none"),
    #     (3, "three seconds"),
    #     (5, "five seconds"),
    #     (10, "ten seconds")
    # ]
    # increment = models.IntegerChoices(increment_choices, default=0)
    time_amount = models.IntegerField()
    increment = models.IntegerField()