from django.urls import path
from .views import UserProfileViewSet
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path("profile/", UserProfileViewSet.as_view({
        "get" : "profile_details",
        "post" : "create",
        "put" : "update",
        "delete" : "destroy",
    }), name="profile"),

    path("profile/<str:id>/", UserProfileViewSet.as_view({
        "get" : "profile_details",
        "put" : "update",
        "delete" : "destroy",
    }), name="userprofile")



    
] 
