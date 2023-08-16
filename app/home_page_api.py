from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from core.models import Booking




class HomePageAPIViewSet(views.APIView):


    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_latest_appointment(self):

        lt_app = Booking.objects.filter(patient=self.request.user.user_profile).order_by('appointment__appointment_date_time').last()
        if lt_app is None:
            return None
        else:
            return {
                "appointment_date_time" : lt_app.appointment.appointment_date_time,
                "doctor_name" : lt_app.doctor.doctor_name,
                "doctor_id" : lt_app.doctor_id,
                "amount" : lt_app.payment.amount,
                "speciality" : lt_app.doctor.doctor_speciality,
                "appointment_id" : lt_app.appointment_id
            }
        
    def get_banner_photos(self):
        ##
        return [
            {
                "image_url" : "",
                "action_url" : ""
            }
        ]
    

    def get_top_doctors(self):
        return None
    
    def get_top_pharmacies(self):
        return None
    
    def get_top_categories(self):
        return None
    
    def get_profile_data(self):
        return {
            "full_name" : self.request.user.user_profile.full_name,
            "email" : self.request.user.email
        }

    def get(self, request):

        response = {
            "latest_appointment" : self.get_latest_appointment(),
            "banners" : self.get_banner_photos(),
            "top_doctors" : self.get_top_doctors(),
            "top_pharmacies" : self.get_top_pharmacies(),
            "top_categories" : self.get_top_categories(),
            "profile_data" : self.get_profile_data()
        }
        return Response(response, status=status.HTTP_200_OK)