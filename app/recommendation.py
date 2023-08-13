from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from doctor.models import Doctor
from pharmacy.models import PharmacyUser, Pharmacy
from django.db.models import Q, F
from .serializers import PharmacyDataSerializer, DoctorDataSerializer, RecomendationRequestSerializer
import math


MAX_DISTANCE = 20



def calculate_distance(lat1, lng1, lat2, lng2):
    R = 6371  # radius of the earth in km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *  math.sin(dlng / 2) * math.sin(dlng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_pharmacy_to_user(request):
    profile = request.user.userprofile
    serializer = RecomendationRequestSerializer(data=request.data)
    if serializer.is_valid():
        lat = request.data.get('lat')
        lng = request.data.get('lng')

        lat_min = lat - (MAX_DISTANCE / 111.0)
        lat_max = lat + (MAX_DISTANCE / 111.0)
        lng_min = lng - (MAX_DISTANCE / (111.0 * math.cos(math.radians(lat))))
        lng_max = lng + (MAX_DISTANCE / (111.0 * math.cos(math.radians(lat))))

        nearby_pharmacies = Pharmacy.objects.filter(
            lat__range=(lat_min, lat_max),
            lng__range=(lng_min, lng_max)
        ).annotate(distance=calculate_distance(lat, lng, F('lat'), F('lng')))
    
        return Response({
            'cat' : 'pharmacy',
            'total' : len(nearby_pharmacies),
            'data' : PharmacyDataSerializer(nearby_pharmacies, many=True)
        }, status=200)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_doctor_to_user(request):
    profile = request.user.userprofile


    
    return Response({
        'type' : 'doctor',
        'data' : {
        }
    }, status=200)

