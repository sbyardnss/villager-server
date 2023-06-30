from django.db import models


class GuestPlayer(models.Model):
    name = models.CharField(max_length=50, default="Bob Ross")
    @property
    def guest_id(self):
        return f'g{self.pk}'
