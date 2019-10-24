from rest_framework import serializers
from app.models import Ticket, Place, Point, User
import logging

log = logging.getLogger(__name__)


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
    timestamp = serializers.IntegerField(source='get_timestamp')

    class Meta:
        model = Ticket
        fields = ["id", "title", "description", "date_time", "point", "timestamp",
                  "speed_test", "wifi_points", "status", "label", "author"]


class TicketCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ["title", "description", "location_point", "user",
                  "speed_test", "wifi_points", "id"]

    def create(self, validated_data):
        log.debug("TicketCreateSerializer:create")
        instance = Ticket()
        title = validated_data.get('title', "No Title")
        description = validated_data.get('description', "No Description")
        user = validated_data.get('user', None)
        speed_test = validated_data.get("speed_test", None)
        wifi_points = validated_data.get("wifi_points", None)
        location_point = validated_data.get("location_point", None)

        instance.title = title
        instance.description = description
        instance.user = user if user else None
        instance.speed_test = speed_test
        instance.wifi_points = wifi_points
        instance.location_point = location_point
        instance.save()
        return instance
