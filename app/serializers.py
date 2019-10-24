from rest_framework import serializers
from app.models import Ticket, Place, Point


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"


class PointSerializer(serializers.ModelSerializer):
    location = PlaceSerializer(read_only=True, many=False, source='get_location')

    class Meta:
        model = Point
        fields = ["id", "x", "y", "location"]


class TicketSerializer(serializers.ModelSerializer):
    author = serializers.DictField(source='get_author')
    point = PointSerializer(read_only=True, many=False, source='get_point')
    label = serializers.DictField(source='get_label')

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "date_time", "point",
                  "speed_test", "wifi_points", "status", "label", "author"]





