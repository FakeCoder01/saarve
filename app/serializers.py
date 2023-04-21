from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = UserProfile
        fields = ["id", "email", "full_name", "profile_pic", "age", "gender", "phone", "city", "pincode", "address", "created_at", "last_updated_at"]
        # fields = "__all__"
