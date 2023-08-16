from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import AppointmentDisplayShowSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from core.models import Appointment, Booking




class AppointmentViewSet(viewsets.ModelViewSet):

    serializer_class = AppointmentDisplayShowSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        return 
    
    def appointment_details(self, request, id=None):
        if id is None:
            bookings = Booking.objects.filter(profile=self.request.user.user_profile)
            serializer = self.get_serializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if not Appointment.objects.filter(id=id, profile=self.request.user.user_profile).exists():
           return Response({"message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        appointment_booking = Appointment.objects.get(id=id).appointment_booking_detials
        
        booking_serializer = self.get_serializer(appointment_booking)
        return Response(booking_serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, requsest, id):
        if not Appointment.objects.filter(id=id, profile=self.request.user.user_profile).exists():
           return Response({"message" : "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        Appointment.objects.get(id=id).delete()
        return Response({"message" : "deleted"}, status=status.HTTP_204_NO_CONTENT)