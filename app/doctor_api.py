from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from doctor.models import Doctor, DoctorReview
from .serializers import DoctorReviewSerializer, DoctorOverviewSerializer, PharmacyDataSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class DoctorReviewViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return DoctorReview.objects.filter(doctor__id=self.doctor_id)


    def review_details(self, request, doctor_id):
        self.doctor_id = doctor_id
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self, request, doctor_id):
        try:
            if not Doctor.objects.filter(id=doctor_id).exists():
                return Response({'detail' : 'no doctor found'}, status=404)
            doctor = Doctor.objects.get(id=doctor_id)
            if DoctorReview.objects.filter(doctor=doctor, user=self.request.user.user_profile).exists():
                return Response({'detail' : 'already reviewd'}, status=401)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(doctor=doctor, user=self.request.user.user_profile)
                return Response(serializer.data, status=201)
            return Response({"detail" : "All fields are neccessary"}, status=400)
        
        except Exception as err:
            print(err)
            return Response({'detail' : 'something went wrong'}, status=500)   
    
    def destroy(self, request):
        
        if request.data.get('id') != None:
            id = request.data.get('id')
            try:
                review = DoctorReview.objects.get(id=id, user=self.request.user.user_profile)
                review.delete()
                return Response({'detail' : 'deleted'}, status=200)
            except Exception as err:
                print(err)
                return Response({'detail' : 'error'}, status=400)   


class DoctorOverviewDetailsViewset(viewsets.ModelViewSet):
    serializer_class = DoctorOverviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)


    def get_queryset(self):
        return DoctorReview.objects.filter(doctor__id=self.doctor_id)

    def doctor_details(self, request, doctor_id):
        self.doctor_id = doctor_id
        queryset = Doctor.objects.get(id=doctor_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=200)
    



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def pharmacies_for_a_doctor(request, doctor_id):
    if not Doctor.objects.filter(id=doctor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    doctor = Doctor.objects.get(id=doctor_id)
    serializer = PharmacyDataSerializer(doctor.pharmacies.all(), many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)