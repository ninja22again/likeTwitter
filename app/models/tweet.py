from django.db import models
from . import User


class Tweet(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=280)
    is_active = models.BooleanField(default=True)
    is_retweet = models.BooleanField(default=False)
    retweets = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
