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

    title = models.TextField(max_length=255, null=False, blank=False, verbose_name="Title")
    description = models.TextField(max_length=2000, null=True, blank=False, verbose_name="Description")
    point = models.ForeignKey('Point', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Map Point")
    speed_test = JSONField(blank=True, null=True, verbose_name="Speed Test")
    load_test = JSONField(blank=True, null=True, verbose_name="Load Tests")
    points = JSONField(blank=True, null=True, verbose_name="Wifi Points List")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="User")
    status = models.CharField(choices=STATUS_CHOICES, default=TO_DO, max_length=10, verbose_name="Ticker Status")
    label = models.CharField(choices=LABEL_CHOICES, default=LABEL_UNLABELED, max_length=20, verbose_name="Description")

    def __str__(self):
        return str(self.id) + ":[" + self.title + "]"


class Place(models.Model):
    img = models.ImageField(blank=False, null=False, verbose_name="Image")
    city = models.CharField(max_length=50, null=False, verbose_name="City")
    address = models.TextField(blank=True, null=True, max_length=255, verbose_name="Address")
    floor = models.IntegerField(blank=True, null=True, verbose_name="Floor")

    def __str__(self):
        return str(self.id) + ":[" + self.city + ":" + self.address + ":" + str(self.floor) + "]"


class Point(models.Model):
    x = models.FloatField(blank=True, null=True, verbose_name="X position")
    y = models.FloatField(blank=True, null=True, verbose_name="Y Position")
    place = models.ForeignKey('Place', blank=False, null=False, on_delete=models.CASCADE, verbose_name="Location")

    def __str__(self):
        return str(self.id) + ":[" + str(self.place) + "|x:" + str(self.x) + "; y:" + str(self.y) + "]"
