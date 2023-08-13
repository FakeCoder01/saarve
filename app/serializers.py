from rest_framework import serializers
from .models import UserProfile
from pharmacy.models import Pharmacy, PharmaReview
from doctor.models import Doctor, DoctorReview, DoctorSchedule
from core.models import Appointment, Booking


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model = UserProfile
        fields = ["id", "email", "full_name", "profile_pic", "age", "gender", "phone", "city", "pincode", "address", "created_at", "last_updated_at"]
        # fields = "__all__"


### for search/recommenadtion format

class PharmacyDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.pharmacy_extd.name")
    total_no_docs = serializers.IntegerField(source="pharmacy.get_num_of_docs") # Pharmacy()
    class Meta:
        model = Pharmacy   
        fields = [
            "pharmacy_profile_pic", "name", "pharmacy_city", "pharmacy_pincode", "pharmacy_description", "total_no_docs", "pharmacy_rating"
        ]

class DoctorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id", "doctor_profile_pic", "doctor_name", "doctor_speciality", "doctor_rating", "doctor_fees", "doctor_degree"
        ]

class RecomendationRequestSerializer(serializers.ListSerializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()
    class Meta:
        fields = [
            "lat", "lng"
        ]        


## deatiled page format [doctor]
class DoctorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorReview
        fields = "__all__"

class DoctorOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"   

## deatiled page format [pharmacy]
class PharmacyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmaReview
        fields = "__all__"

class PharmacyOverviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"   


class DoctorScheduleSerializer(serializers.ModelSerializer):
    expected_appointment_time = serializers.DateTimeField()
    class Meta:
        model = DoctorSchedule
        fields = ("id", "doctor", "pharmacy", "start_time", "end_time", "duration", "total_booked", "fees", "expected_appointment_time")

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class AppointmentBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"