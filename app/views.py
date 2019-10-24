from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response, status
from app.serializers import TicketSerializer, PlaceSerializer, PointSerializer
from app.models import Ticket, Place, Point
from rest_framework.parsers import FormParser, MultiPartParser, FileUploadParser, JSONParser
# Create your views here.


class TicketModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']
    queryset = Ticket.objects.all()
    parser_classes = (JSONParser,)
    serializers = {
        'default': TicketSerializer,
        'get_status_lit': TicketSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(methods=['get'], detail=False)
    def get_status_lit(self, request):
        return Response({"status_list": [{x[0]:x[1]} for x in Ticket.STATUS_CHOICES]}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False)
    def get_labels_list(self, request):
        return Response({"label_list": [{x[0]:x[1]} for x in Ticket.LABEL_CHOICES]}, status=status.HTTP_200_OK)


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
