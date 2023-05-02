from django.db import models
from django.utils.crypto import get_random_string
from doctor.models import Doctor, DoctorSchedule
from pharmacy.models import Pharmacy
from app.models import UserProfile
import uuid


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)
    amount = models.FloatField()
    method = models.CharField(default="online", max_length=8)
    status = models.CharField(default="Initiated", max_length=10)
    is_verified = models.BooleanField(default=False)
    payment_id = models.CharField(default=get_random_string(10), unique=True, max_length=10)

    def __str__(self) -> str:
        return self.payment_id
    
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

    schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE, related_name="schedule_appointment_details")
    appointment_date_time = models.DateTimeField()
    no_in_queuee = models.PositiveIntegerField(default=1)
    
    patient_name = models.CharField(max_length=60, null=True, blank=True)
    patient_age = models.PositiveIntegerField(null=True, blank=True)
    patient_gender = models.CharField(default="Male", max_length=8)

    note = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.patient_name
    
class Booking(BaseModel):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="patient_booking_profile")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_booking_profile")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="pharmacy_booking_profile")
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="payment_booking_details")
    appointment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="appointment_booking_detials")