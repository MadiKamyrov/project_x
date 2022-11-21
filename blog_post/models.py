from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    like = models.ManyToManyField(User, blank=True, related_name="like")
    unlike = models.ManyToManyField(User, blank=True, related_name="unlike")
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publisher")
    like_count = models.IntegerField(default=0, blank=True)
    unlike_count = models.IntegerField(default=0, blank=True)