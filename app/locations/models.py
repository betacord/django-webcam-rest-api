from django.db import models


class Continent(models.Model):
    """Continent model"""
    name = models.CharField(max_length=256, unique=True)


class Country(models.Model):
    """Country model"""
    name = models.CharField(max_length=256, unique=True)
    continent = models.ForeignKey(Continent, null=True, on_delete=models.CASCADE)
