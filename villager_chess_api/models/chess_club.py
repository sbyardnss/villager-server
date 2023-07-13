from django.db import models


class ChessClub(models.Model):
    name = models.CharField(max_length=30)
    manager = models.ForeignKey(
        'Player', on_delete=models.SET_NULL, related_name='created_clubs', null=True)
    date = models.DateField(auto_now=True)
    address = models.CharField(max_length=75, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=5, null=True)
    zipcode = models.PositiveIntegerField(null=True)
    details = models.CharField(null=True, max_length=100)
    password = models.CharField(null=True, max_length=20)
    members = models.ManyToManyField('Player', related_name='my_clubs')
    guest_members = models.ManyToManyField('GuestPlayer', related_name='selected_guests_tournaments')