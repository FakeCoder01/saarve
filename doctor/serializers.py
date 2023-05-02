from rest_framework import serializers
from .models import Doctor, DoctorReview, DoctorSchedule

class DoctorProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = Doctor
        fields = ["email", "doctor_name", "doctor_degree", "doctor_reg_no", "doctor_gender", "doctor_speciality", "doctor_phone", "doctor_description", "doctor_profile_pic", "doctor_services", "doctor_work_experience", "doctor_fees", "doctor_rating", "", ""]
        # fields = "__all__"