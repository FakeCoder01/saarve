from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("user/login/", ObtainAuthToken.as_view(), name='api_token_auth'),
] 
