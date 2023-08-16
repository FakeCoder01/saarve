from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from pharmacy.models import Pharmacy, PharmaReview
from .serializers import PharmacyReviewSerializer, PharmacyOverviewSerializer, DoctorDataSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class PharmacyReviewViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacyReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return PharmaReview.objects.filter(pharmacy__id=self.pharmacy_id)


    def review_details(self, request, pharmacy_id):
        self.pharmacy_id = pharmacy_id
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pharmacy_id):
        try:
            if not Pharmacy.objects.filter(id=pharmacy_id).exists():
                return Response({'detail' : 'no pharmacy found'}, status=status.HTTP_404_NOT_FOUND)
            pharmacy = Pharmacy.objects.get(id=pharmacy_id)
            if PharmaReview.objects.filter(pharmacy=pharmacy, user=self.request.user.user_profile).exists():
                return Response({'detail' : 'already reviewd'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(pharmacy=pharmacy, user=self.request.user.user_profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail" : "All fields are neccessary"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as err:
            print(err)
            return Response({'detail' : 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
    
    def destroy(self, request):
        
        if request.data.get('id') != None:
            id = request.data.get('id')
            try:
                review = PharmaReview.objects.get(id=id, user=self.request.user.user_profile)
                review.delete()
                return Response({'detail' : 'deleted'}, status=status.HTTP_204_NO_CONTENT)
            except Exception as err:
                print(err)
                return Response({'detail' : 'error'}, status=status.HTTP_400_BAD_REQUEST)   


class PharmacyOverviewDetailsViewset(viewsets.ModelViewSet):
    serializer_class = PharmacyOverviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return PharmaReview.objects.filter(pharmacy__id=self.pharmacy_id)

    def pharmacy_details(self, request, pharmacy_id):
        self.pharmacy_id = pharmacy_id
        queryset = Pharmacy.objects.get(id=pharmacy_id)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def doctors_in_a_pharmacy(request, pharmacy_id):
    if not Pharmacy.objects.filter(id=pharmacy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    serializer = DoctorDataSerializer(pharmacy.doctor_set.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)