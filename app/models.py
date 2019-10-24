from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.


class Ticket(models.Model):
    title = models.TextField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=2000, null=True, blank=False)


class Scan(models.Model):
    speed_test = JSONField(blank=True, null=True)


class Place(models.Model):
    img = models.ImageField(blank=False, null=False)
    city = models.CharField(max_length=50, null=False)
    floor = models.IntegerField(blank=True, null=True)

class Point*()