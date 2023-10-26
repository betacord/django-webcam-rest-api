from django.db import models


class Continent(models.Model):
    name = models.CharField(max_length=256)


class Country(models.Model):
    name = models.CharField(max_length=256)
    continent = models.ForeignKey(Continent, null=True, on_delete=models.CASCADE)
