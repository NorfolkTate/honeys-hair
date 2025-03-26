from django.contrib import admin

# Register your models here.

from .models import Booking, Service

admin.site.register(Booking)
admin.site.register(Service)
