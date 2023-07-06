from django.db import models
from villager_chess_api.models import Game
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('Player', related_name='followers')
    games = GenericRelation(Game)
    @property
    def full_name(self):
        """full name custom property"""
        return f'{self.user.first_name} {self.user.last_name}'
    @property
    def email(self):
        return self.user.email
    @property
    def username(self):
        return self.user.username
    @property
    def password(self):
        return self.user.password
    @property
    def first_name(self):
        return self.user.first_name
    @property
    def last_name(self):
        return self.user.last_name
    @property
    def is_friend(self):
        return self.__is_friend
    @is_friend.setter
    def is_friend(self, value):
        self.__is_friend = value