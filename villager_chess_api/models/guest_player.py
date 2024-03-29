from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from villager_chess_api.models import Game


class GuestPlayer(models.Model):
    full_name = models.CharField(max_length=50, default="Bob Ross")
    games = GenericRelation(Game)
    @property
    def guest_id(self):
        return f'g{self.pk}'
