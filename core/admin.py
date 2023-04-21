from django.contrib import admin
from .models import Payment, Booking, Appointment

# Register your models here.

admin.site.register(Payment)
admin.site.register(Appointment)
admin.site.register(Booking)
