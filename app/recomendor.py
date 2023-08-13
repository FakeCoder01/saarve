from pharmacy.models import Pharmacy
from doctor.models import Doctor
from django.db.models import Q 
from .serializers import PharmacyDataSerializer, DoctorDataSerializer, RecomendationRequestSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
import math
from collections import defaultdict

# constants
MAX_DISTANCE = 60

def calculate_distance(lat1, lng1, lat2, lng2):
    # calculate the distance between two sets of latitude and longitude coordinates
    # using the Haversine formula to calculate distance   
    R = 6371  # radius of the earth in km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *  math.sin(dlng / 2) * math.sin(dlng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance


class Recommendation(viewsets.ModelViewSet):
    serializer_class = RecomendationRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)


    def get_pharmacy_recommendations(self, lat, lng):

        lat_min = lat - (MAX_DISTANCE / 111.0)
        lat_max = lat + (MAX_DISTANCE / 111.0)
        lng_min = lng - (MAX_DISTANCE / (111.0 * math.cos(math.radians(lat))))
        lng_max = lng + (MAX_DISTANCE / (111.0 * math.cos(math.radians(lat))))

        nearby_pharmacies = Pharmacy.objects.filter(
            lat__range=(lat_min, lat_max),
            lng__range=(lng_min, lng_max)
        )
        serializer = PharmacyDataSerializer(nearby_pharmacies, many=True)
        return serializer.data
    
    def get_doctor_recommendations(self):
        user = self.request.user.user_profile

        nearby_doctors = Doctor.objects.filter(
            Q(doctor_address__icontains = user.city) |
            Q(doctor_address__icontains = user.address) 
        )

        serializer = DoctorDataSerializer(nearby_doctors, many=True)
        return serializer.data
    
    def generate_recommendations(self, request):
        lat = request.data.get("lat")
        lng = request.data.get("lng")
        doctors = self.get_doctor_recommendations()
        pharmacies = self.get_pharmacy_recommendations(lat, lng)

        return Response({
            "data" : {
                "pharmacies" : pharmacies,
                "doctors" : doctors
            }
        }, status=200)

