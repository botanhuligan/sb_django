from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from app.serializers import TicketSerializer, PlaceSerializer, PointSerializer
from app.models import Ticket, Place, Point
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
# Create your views here.


class TicketModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']
    queryset = Ticket.objects.all()
    parser_classes = (JSONParser,)
    serializers = {
        'default': TicketSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class PlaceModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']
    queryset = Place.objects.all()
    parser_classes = (JSONParser,)
    serializers = {
        'default': PlaceSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])


class PointModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Point.objects.all()
    parser_classes = (JSONParser,)
    serializers = {
        'default': PointSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
