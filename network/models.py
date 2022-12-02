from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass

# If user override doesn't work with the M2M field, we can instead split it up into a different table.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,  blank=True, related_name="follower_user")
    following = models.ManyToManyField(User,  blank=True, related_name="following_user")

    def __str__(self):
        return self.user.username

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.CharField(max_length=280, null=True, blank = True)
    comment = models.CharField(max_length=280, null=True, blank = True)
    like = models.ManyToManyField(User, blank=True, related_name="liked_user")
    created_at = models.DateTimeField(auto_now=True)
