from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import views
from .views import PharmacyProfileViewSet

urlpatterns = [
    path("user/login/", ObtainAuthToken.as_view(), name='api_token_auth'),
    path("user/signup/", views.sign_up_register, name='sign_up_register'),
    path("user/verify/", views.otp_verification, name='otp_verification'),

    path("profile/", PharmacyProfileViewSet.as_view({
        "get" : "profile_details",
        "post" : "create",
        "put" : "update",
        "delete" : "destroy",
    }), name="pharmacy_profile_view_set"),
    




] 

