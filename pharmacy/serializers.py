from rest_framework import serializers
from .models import Pharmacy, PharmaReview, PharmacyUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from doctor.models import Doctor

class PharmacyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [ "pharmacy_profile_pic", "pharmacy_pincode", "pharmacy_city", "pharmacy_address", "pharmacy_description", "pharmacy_phone"]
        # fields = "__all__"



class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.IntegerField(source="PharmacyUser.phone_number")
    name = serializers.CharField(source="PharmacyUser.name")
    phramacy_reg_no = serializers.CharField(source="PharmacyUser.phramacy_reg_no")
    confirm_password = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'password', 'confirm_password', 'phone_number', 'phramacy_reg_no')

class OTPVerificationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="User.email")
    class Meta:
        model = PharmacyUser
        fields = ('email', 'phone_number', 'email_otp', 'phone_otp')                


