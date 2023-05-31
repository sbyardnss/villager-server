from django.db import models

class Tournament(models.Model):
    """tournament model"""
    title = models.CharField(max_length=50)
    date = models.DateField()
    time_setting = models.ForeignKey('TimeSetting', on_delete=models.SET_NULL, default=0, related_name="tournaments_with_time_setting")


# table tournament {
#   id int pk
#   datetime datetime
#   title varchar
#   timesetting_id int
# }