from django.db import models

# Create your models here.

"""Model Definition for house"""


class House(models.Model):
    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pets_allowed = models.BooleanField(default=True)
