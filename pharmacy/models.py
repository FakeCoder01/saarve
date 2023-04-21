from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

class Pharmacy(BaseModel):
    user = models.OneToOneField(User, related_name="pharmacy_profile", on_delete=models.CASCADE)

    pharmacy_name = models.CharField(max_length=60)
    pharmacy_profile_pic = models.ImageField(upload_to="pharmacy/profile/")
    pharmacy_reg_no = models.CharField(max_length=20)

    pharmacy_pincode = models.IntegerField()
    pharmacy_city = models.CharField(max_length=60)
    pharmacy_address = models.CharField(max_length=200)
    pharmacy_description = models.TextField()

    pharmacy_phone = models.CharField(max_length=60)
    pharmacy_rating = models.FloatField(default=0)

    is_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.pharmacy_name
    
    def get_pharmacy_images(self):
        return {
            "images" : list(PharmacyImage.objects.filter(pharmacy=self).values_list()) 
        }
    
    def get_pharmacy_reviews(self):
        return {
            "reviews" : list(PharmaReview.objects.filter(pharmacy=self).values())
        }
    
    

class PharmacyImage(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, related_name="pharmacy_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="pharmacy/images/")

class PharmaReview(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="pharmacy_review")
    review = models.TextField()
    user = models.CharField(max_length=60)
    created_at = models.DateField(auto_now=True)    