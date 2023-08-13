from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from doctor.models import Doctor
from pharmacy.models import Pharmacy
from django.db.models import Q
from .serializers import PharmacyDataSerializer, DoctorDataSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_and_filter_doctor_and_pharmacy(request):

    q = request.data.get('q')
    cat = request.data.get('catagory')
    speciality = request.data.get('speciality')
    rating = request.data.get('rating')
    fee = request.data.get('fee')
    sex = request.data.get('sex')

    if q is None:
        return Response({"msg" : "q required"}, status=400)

    if cat == 'doctor':
        docs = Doctor.objects.filter(
            Q(doctor_name__icontains = q) |
            Q(doctor_description__icontains = q) |
            Q(doctor_work_experience__icontains = q) |
            Q(doctor_services__icontains = q) |
            Q(doctor_address__icontains = q)
        )
        if speciality is not None:
            docs = docs.filter(doctor_speciality = speciality)
        if sex is not None:
            docs = docs.filter(doctor_gender = sex)   
        if rating is not None:
            docs = docs.filter(doctor_rating__range=(rating, rating+10))
        if fee is not None:
            docs = docs.filter(doctor_fees__range=(fee, fee+10))

        serializer = DoctorDataSerializer(docs, many=True)
        return Response({
            'cat' : 'doctor',
            'data' : {
                'doctors' : serializer.data
            }
        }, status=200)
    

    elif cat == 'pharmacy':
        pharmacies = Pharmacy.objects.filter(
            Q(user__pharmacy_extd__name__icontains = q) |
            Q(pharmacy_description__icontains = q) |
            Q(pharmacy_city__icontains = q) |
            Q(pharmacy_address__icontains = q)
        )
        if rating is not None:
            docs = pharmacies.filter(pharmacy_rating__range=(rating, rating+10))
        serializer = PharmacyDataSerializer(data=pharmacies, many=True)
        return Response({
            'cat' : 'pharmacy',
            'data' : {
                'pharmacies' : serializer.data
            }
        }, status=200)
    
    else:
        pharmacies = pharmacies = Pharmacy.objects.filter(
            Q(user__pharmacy_extd__name__icontains = q) |
            Q(pharmacy_description__icontains = q) |
            Q(pharmacy_city__icontains = q) |
            Q(pharmacy_address__icontains = q)
        )
        if rating is not None:
            docs = pharmacies.filter(pharmacy_rating__range=(rating, rating+10))
        
        docs = Doctor.objects.filter(
            Q(doctor_name__icontains = q) |
            Q(doctor_description__icontains = q) |
            Q(doctor_work_experience__icontains = q) |
            Q(doctor_services__icontains = q) | 
            Q(doctor_address__icontains = q)
        )
        if speciality is not None:
            docs = docs.filter(doctor_speciality = speciality)
        if sex is not None:
            docs = docs.filter(doctor_gender = sex)   
        if rating is not None:
            docs = docs.filter(doctor_rating__range=(rating, rating+10))
        if fee is not None:
            docs = docs.filter(doctor_fees__range=(fee, fee+10))

        return Response({
            'cat' : 'all',
            'data' : {
                'doctors' : DoctorDataSerializer(docs, many=True).data ,
                'pharmacies' : PharmacyDataSerializer(pharmacies, many=True).data
            }
        }, status=200)


