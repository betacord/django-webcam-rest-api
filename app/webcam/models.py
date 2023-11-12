from django.db import models

from locations.models import Country
from user.models import User


class Category(models.Model):
    """Webcam category model"""
    name = models.CharField(max_length=512)


class Webcam(models.Model):
    """Webcam model"""
    name = models.CharField(max_length=1024)
    description = models.TextField()
    url = models.URLField(max_length=512)
    thumbnail_url = models.URLField(max_length=512)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    """Webcam comment model"""
    content = models.TextField()
    date_added = models.DateField(auto_now=True)
    user_added = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    webcam = models.ForeignKey(Webcam, null=True, on_delete=models.CASCADE)
