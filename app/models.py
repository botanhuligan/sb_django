from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from datetime import datetime
import logging
log = logging.getLogger(__name__)
# Create your models here.
NAME = "name"
TITLE = "title"


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

    STATUS_DICT = {k[0]:k[1] for k in STATUS_CHOICES}

    LABEL_NOT_SEE = 'not_see'
    LABEL_LOW_SIGNAL = 'low_signal'
    LABEL_NOISE = 'noise'
    LABEL_LOST_TRAFFIC = 'lost_traffic'
    LABEL_OTHER = 'other'
    LABEL_UNLABELED = 'unlabeled'


    LABEL_CHOICES = [
        (LABEL_NOT_SEE, 'Not Visible WiFi'),
        (LABEL_LOW_SIGNAL, 'Low Wifi Signal'),
        (LABEL_NOISE, 'Noisy Channels'),
        (LABEL_LOST_TRAFFIC, 'Package Lost'),
        (LABEL_OTHER, 'Other'),
        (LABEL_UNLABELED, 'No Label')
    ]

    LABELS_DICT = {k[0]:k[1] for k in LABEL_CHOICES}

    title = models.TextField(max_length=255, null=False, blank=False, verbose_name="Title", editable=False)
    description = models.TextField(max_length=2000, null=True, blank=False, verbose_name="Description")
    date_time = models.DateTimeField(auto_now=True, auto_created=True, editable=False)
    location_point = models.ForeignKey('Point', null=True, blank=True, on_delete=models.CASCADE, verbose_name= "Map Point")
    speed_test = JSONField(blank=True, null=True, verbose_name="Speed Test")
    wifi_points = JSONField(blank=True, null=True, verbose_name="Wifi Points List")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="User", editable=False, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default=TO_DO, max_length=10, verbose_name="Ticker Status")
    label = models.CharField(choices=LABEL_CHOICES, default=LABEL_UNLABELED, max_length=20, verbose_name="Description")

    def __str__(self):
        # log.debug("Ticket:__str__")
        return str(self.id) + ":[" + self.title + "]"

    def get_author(self):
        # log.debug("Ticket:get_author")
        if self.user:
            return {
              "first_name": self.user.first_name,
              "last_name": self.user.last_name,
              "group": self.user.groups.name,
              "email": self.user.email
            }
        return {
            "first_name": None,
            "last_name": None,
            "group": None,
            "email": None
        }

    def get_point(self):
        # log.debug("Ticket:get_point")
        return self.location_point

    def get_label(self):
        # log.debug("Ticket:get_label")
        return {
            NAME: self.label,
            TITLE: self.LABELS_DICT[self.label]
        }

    def get_status(self):
        return {
            NAME: self.status,
            TITLE: self.STATUS_DICT[self.status]
        }

    def get_timestamp(self):
        # log.debug("Ticket:get_timestamp")
        return self.date_time.timestamp()


class Place(models.Model):
    img = models.ImageField(blank=False, null=False, verbose_name="Image")
    city = models.CharField(max_length=50, null=False, verbose_name="City")
    address = models.TextField(blank=True, null=True, max_length=255, verbose_name="Address")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Floor")

    def __str__(self):
        # log.debug("Place:__str__")
        return str(self.id) + ":[" + self.city + ":" + self.address + ":" + str(self.floor) + "]"


class Point(models.Model):
    x = models.FloatField(blank=True, null=True, verbose_name="X position")
    y = models.FloatField(blank=True, null=True, verbose_name="Y Position")
    place = models.ForeignKey('Place', blank=False, null=False, on_delete=models.CASCADE, verbose_name="Location")

    def __str__(self):
        # log.debug("Point:__str__")
        return str(self.id) + ":[" + str(self.place) + "|x:" + str(self.x) + "; y:" + str(self.y) + "]"

    def get_location(self):
        # log.debug("Point:get_location")
        return self.place
