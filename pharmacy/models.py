from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
import uuid, datetime
from app.models import UserProfile
# Create your models here.


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

class PharmacyUser(models.Model):
    user = models.OneToOneField(User, related_name="pharmacy_extd", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    pharmacy_reg_no = models.CharField(max_length=32)
    phone_number = models.CharField(max_length=20)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    phone_otp = models.CharField(max_length=200, null=True, blank=True)
    email_otp = models.CharField(max_length=200, null=True, blank=True)
    phone_otp_creation = models.DateTimeField(null=True, blank=True)
    email_otp_creation = models.DateTimeField(null=True, blank=True)


    def set_phone_otp(self, code):
        self.phone_otp = make_password(code)
        self.phone_otp_creation = datetime.datetime.now()

    def set_email_otp(self, code):
        self.email_otp = make_password(code)
        self.email_otp_creation = datetime.datetime.now()

    def verify_phone(self, phone_otp):
        #if self.phone_otp_creation > datetime.datetime.now() - datetime.timedelta(minutes=10):
        self.is_phone_verified = True
        return check_password(phone_otp, self.phone_otp)
        #return False
    
    def verify_email(self, email_otp):
        #if  self.email_otp_creation > datetime.datetime.now() - datetime.timedelta(minutes=10):
        self.is_email_verified = True
        return check_password(email_otp, self.email_otp)
        #return False
    

    def __str__(self):
        return self.pharmacy_reg_no
    
    
class Pharmacy(BaseModel):
    user = models.OneToOneField(User, related_name="pharmacy_profile", on_delete=models.CASCADE)
    pharmacy_profile_pic = models.ImageField(upload_to="pharmacy/profile/", default="default/pharmacy-d.jpg")

    pharmacy_pincode = models.IntegerField()
    pharmacy_city = models.CharField(max_length=60)
    pharmacy_address = models.CharField(max_length=200)
    pharmacy_description = models.TextField()

    pharmacy_phone = models.CharField(max_length=60)
    pharmacy_rating = models.FloatField(default=0)

    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.email
    

    
    def get_num_of_docs(self):
        return self.doctor_set.count()

    def get_pharmacy_reviews(self):
        return {
            "reviews" : list(PharmaReview.objects.filter(pharmacy=self).values())
        }
    

class PharmaReview(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="pharmacy_review")
    review = models.TextField()
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="pharmacy_reviewed_by")
    rating = models.PositiveSmallIntegerField(default=0, blank=True)
    created_at = models.DateField(auto_now=True)
