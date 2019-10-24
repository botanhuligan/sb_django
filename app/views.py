from django.shortcuts import render
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response, status
from app.serializers import TicketSerializer, PlaceSerializer, PointSerializer
from app.models import Ticket, Place, Point, NAME, TITLE
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
# Create your views here.
import logging

logger = logging.getLogger("VIEWS")
MESSAGE = 'message'
RESULT = 'result'
FAIL = 'fail'
SUCCESS = 'success'

class TicketModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']
    parser_classes = (JSONParser,)
    serializers = {
        'default': TicketSerializer
    }

    def get_queryset(self):
        return Ticket.objects.all()[:100]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(methods=['get'], detail=False, url_path='status_list')
    @permission_classes([AllowAny])
    def get_status_lit(self, request):
        return Response({"status_list": [{NAME: x[0], TITLE: x[1]} for x in Ticket.STATUS_CHOICES]},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='label_list')
    @permission_classes([AllowAny])
    def get_labels_list(self, request):
        return Response({"label_list": [{NAME: x[0], TITLE: x[1]} for x in Ticket.LABEL_CHOICES]},
                        status=status.HTTP_200_OK)


class PlaceModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post', 'delete']
    queryset = Place.objects.all()
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
