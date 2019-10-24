from rest_framework.serializers import ModelSerializer
from app.models import Ticket, Place, Point


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class PointSerializer(ModelSerializer):
    class Meta:
        model = Point
        fields = "__all__"

