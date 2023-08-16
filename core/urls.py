from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from . import csrf_google

urlpatterns = [
    path('cookie/csrf/', csrf_google.set_csrf_token, name="set_csrf_token"),
    path('auth/google/', csrf_google.google_login_access_token, name="google_login_access_token"),
    path('auth/login/', ObtainAuthToken.as_view(),name="general_login")
] 
