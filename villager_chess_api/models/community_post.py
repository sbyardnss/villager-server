from django.db import models


class CommunityPost(models.Model):
    message = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(
        "Player", on_delete=models.SET_NULL, null=True, related_name="community_posts")
