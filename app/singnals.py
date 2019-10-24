from django.db.models.signals import post_save
from django.dispatch import receiver
from app.models import Ticket
import json


@receiver(post_save, sender=Ticket)
def get_mac(sender, instance, **kwargs):
    data = json.loads(sender.wifi_points)
    print(data)
    print("DEBUuUUUUUUUUUG")