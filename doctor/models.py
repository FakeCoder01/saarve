from django.db import models
from django.contrib.auth.models import User
from pharmacy.models import Pharmacy
import uuid


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

class Doctor(BaseModel):
    user = models.OneToOneField(User, related_name="doctor_profile", on_delete=models.CASCADE)

    doctor_name = models.CharField(max_length=60)
    doctor_degree = models.CharField(max_length=100)
    doctor_reg_no = models.CharField(max_length=20)
    doctor_gender = models.CharField(max_length=8)
    doctor_speciality = models.TextField()
    doctor_phone = models.CharField(max_length=60)
    doctor_description = models.TextField()

    doctor_profile_pic = models.ImageField(upload_to="doctors/profile/", default="default/doctor-d.jpg")
    doctor_services = models.TextField(null=True, blank=True)

    doctor_work_experience = models.TextField(null=True, blank=True) 
    doctor_fees = models.FloatField()
    doctor_rating = models.FloatField(default=0)

    pharmacies = models.ManyToManyField(Pharmacy)

    def __str__(self) -> str:
        return self.doctor_name
    
    def get_doctor_reviews(self):
        return {
            "reviews" : list(DoctorReview.objects.filter(doctor=self).values())
        }
    
class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_review")
    review = models.TextField()
    user = models.CharField(max_length=60)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.user


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_schedule")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="pharmacy_schedule")
    start_time = models.DateTimeField()
    end_time = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=15)
    total_booked = models.PositiveIntegerField(default=0)
    fees = models.FloatField()

    def update_total_booked(self):
        self.total_booked += 1
        return self.total_booked
    

