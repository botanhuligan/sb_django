from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    TO_DO = 'to_do'
    DOING = 'doing'
    DONE = 'done'
    DROP = 'drop'

    STATUS_CHOICES = [
        (TO_DO, 'To Do'),
        (DOING, 'Doing'),
        (DONE, 'Done'),
        (DROP, 'Drop'),
    ]

    title = models.TextField(max_length=255, null=False, blank=False, verbose_name="Description")
    description = models.TextField(max_length=2000, null=True, blank=False)
    point = models.ForeignKey('Point', null=True, blank=True, on_delete=models.CASCADE)
    speed_test = JSONField(blank=True, null=True)
    load_test = JSONField(blank=True, null=True)
    points = JSONField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(choices=STATUS_CHOICES, default=TO_DO, max_length=10)

    def __str__(self):
        return str(self.id) + ":[" + self.title + "]"


# class WifiPoint(models.Model):
#     ssid = models.CharField(max_length=255, null=False, blank=True, default="Unknown")
#     bssid = models.CharField(max_length=20, null=True, blank=True, default="00:00:00:00:00:00")
#     rssi = models.IntegerField(null=True, blank=True)
#     connected = models.BooleanField(null=False, blank=False, default=False)
#     topologyMode = models.TextField(max_length=255, null=True, blank=True)
#     availableWps = models.BooleanField(null=True, blank=True, default=False)
#     isVisible = models.BooleanField(null=True, blank=True, default=False)
#     frequency = models.IntegerField(null=True, blank=True, default=0)
#     channel = models.IntegerField(null=False, blank=False)


class Place(models.Model):
    img = models.ImageField(blank=False, null=False)
    city = models.CharField(max_length=50, null=False)
    address = models.TextField(blank=True, null=True, max_length=255)
    floor = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ":[" + self.city + ":" + self.address + ":" + str(self.floor) + "]"


class Point(models.Model):
    x = models.FloatField(blank=True, null=True)
    y = models.FloatField(blank=True, null=True)
    place = models.ForeignKey('Place', blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ":[" + str(self.place) + "|x:" + str(self.x) + "; y:" + str(self.y) + "]"
