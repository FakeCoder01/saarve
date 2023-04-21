from rest_framework import serializers
from .models import Pharmacy, PharmacyImage, PharmaReview

class PharmacyProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Pharmacy
        fields = ["id", "email", "pharmacy_name", "pharmacy_profile_pic", "profile_pic", "pharmacy_reg_no", "pharmacy_pincode", "pharmacy_city", "pharmacy_address", "pharmacy_description", "pharmacy_phone"]
        # fields = "__all__"
