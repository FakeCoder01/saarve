from django.contrib import admin
from .models import Doctor, DoctorReview, DoctorSchedule
# Register your models here.

admin.site.register(Doctor)
admin.site.register(DoctorReview)
admin.site.register(DoctorSchedule)
