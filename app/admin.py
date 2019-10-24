from django.contrib import admin
from .models import Ticket, AP, WifiAP, Device, MobileAP
# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(AP)
class APAdmin(admin.ModelAdmin):
    pass

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass

@admin.register(WifiAP)
class WifiApAdmin(admin.ModelAdmin):
    pass

@admin.register(MobileAP)
class MobileAPAdmin(admin.ModelAdmin):
    pass

