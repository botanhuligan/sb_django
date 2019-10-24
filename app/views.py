from django.shortcuts import render
from rest_framework.decorators import action, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response, status
from app.serializers import TicketSerializer, PlaceSerializer, PointSerializer, TicketCreateSerializer
from app.models import Ticket, Place, Point, NAME, TITLE
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# Create your views here.
import logging



log = logging.getLogger(__name__)
MESSAGE = 'message'
RESULT = 'result'
FAIL = 'fail'
SUCCESS = 'success'


class TicketModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post']
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = (JSONParser,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers = {
        'default': TicketSerializer,
        'create': TicketCreateSerializer
    }

    def get_queryset(self):
        return Ticket.objects.all()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    @action(methods=['get'], detail=False, url_path='status_list')
    def get_status_list(self, request):
        log.debug("TicketModelViewSet:get_status_list")
        return Response({"status_list": [{NAME: x[0], TITLE: x[1]} for x in Ticket.STATUS_CHOICES]},
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='label_list')
    def get_labels_list(self, request):
        log.debug("TicketModelViewSet:get_labels_list")
        return Response({"label_list": [{NAME: x[0], TITLE: x[1]} for x in Ticket.LABEL_CHOICES]},
                        status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        log.debug("TicketModelViewSet:create")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["user"] = request.user
        obj = serializer.create(validated_data)
        return Response({"id": obj.id}, status=status.HTTP_200_OK)


class PlaceModelViewSet(ModelViewSet):
    http_method_names = ['get']
    queryset = Place.objects.all()
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])
