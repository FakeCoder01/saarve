from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateField(auto_now_add=True)
    last_updated_at = models.DateField(auto_now=True)

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")

    full_name = models.CharField(max_length=60)
    profile_pic = models.ImageField(upload_to="user/profile/", default="default/d-user.jpg", null=True, blank=True)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=8, default="Male", null=True, blank=True)
    phone = models.IntegerField()
    city = models.CharField(max_length=16)
    pincode = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.full_name 