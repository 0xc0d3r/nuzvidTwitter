from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User)
    message = models.CharField(max_length = 140, null = False, blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.user.username + " " + self.message
    
class Follower(models.Model):
    user = models.ForeignKey(User, related_name = 'followee')
    follower = models.ForeignKey(User, related_name =  'follower')
    timestamp = models.DateTimeField(auto_now_add = True)
    
    def __unicode__(self):
        return self.user.username + "is follwoed by" + self.follower.username
