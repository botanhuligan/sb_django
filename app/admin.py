from django.contrib import admin
from app.models import Ticket, Place, Point
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    pass

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass