from django.shortcuts import render
from rest_framework.decorators import action, api_view
from django.contrib import auth
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response, status
from app.serializers import TicketSerializer, PlaceSerializer, PointSerializer, TicketCreateSerializer, \
    TickerUpdateSerializer
from django.views.decorators.csrf import csrf_exempt
from app.models import Ticket, Place, Point, NAME, TITLE
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
# Create your views here.
import logging
from rest_framework.authtoken.models import Token
from app.utils import get_data_by_mac


log = logging.getLogger(__name__)
MESSAGE = 'message'
RESULT = 'result'
FAIL = 'fail'
SUCCESS = 'success'


@api_view(http_method_names=["GET"])
def get_token(request, *args, **kwargs):
    if request.user.is_authenticated:
        return Response({}, status=status.HTTP_200_OK)


@api_view(http_method_names=["POST"])
def get_device_info(request, *args, **kwargs):
    mac = request.data.get("mac")
    if not mac:
        return Response({RESULT: FAIL, MESSAGE: "mac address required!"}, status=status.HTTP_400_BAD_REQUEST)
    data = get_data_by_mac(mac)
    print("data: ", data)
    if not data:
        return Response({RESULT: FAIL, MESSAGE: "Device not found"}, status=status.HTTP_204_NO_CONTENT)
    return Response(data, status=status.HTTP_200_OK)



@api_view(http_method_names=["POST"])
def log_in(request, *args, **kwarg):
    log.debug("log_in:")
    # if request.user.is_authenticated:
    #     log.debug("log_in:user is_authenticated:" + str(request.user))
    #     return Response({"status": "already authenticated"}, status=status.HTTP_200_OK)
    username = request.data.get("username")
    password = request.data.get("password")
    log.debug("log_in:username:" + str(username))
    log.debug("log_in:password:" + str(password))
    if not username or not password:
        return Response({RESULT: FAIL, "error": "password and username fields required"}, status=status.HTTP_400_BAD_REQUEST)
    user = auth.authenticate(request, username=username, password=password)


    if user:
        log.debug("log_in:user exists")
        log.debug("log_in:user id:" + str(user.id))
        auth.login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({RESULT: SUCCESS, "token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({RESULT: "fail! Bad auth data"}, status=status.HTTP_401_UNAUTHORIZED)


class TicketModelViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'post']
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = (JSONParser,)
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializers = {
        'default': TicketSerializer,
        'create': TicketCreateSerializer,
        'update': TickerUpdateSerializer
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

    @action(methods=['post'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        log.debug("TicketModelViewSet:search")
        query = request.data.get("query", None)
        if not query:
            return Response({RESULT: FAIL, MESSAGE: "query field required"}, status=status.HTTP_400_BAD_REQUEST)
        objects = Ticket.objects.filter(description__contains=query)
        if not objects:
            return Response({RESULT: FAIL, MESSAGE: "No tickets found"}, status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
