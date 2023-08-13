from django.urls import path
from .views import UserProfileViewSet
from . import search
from .recomendor import Recommendation
from . import pharmacy_api, doctor_api, appointment


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
    }), name="userprofile"),

    path("recommend/", Recommendation.as_view({
        "get" : "generate_recommendations"
    }), name="recommendation"),

    path("search/", search.search_and_filter_doctor_and_pharmacy, name="search"),


    ## doctor
    path("doctor/<str:doctor_id>/", doctor_api.DoctorOverviewDetailsViewset.as_view({
        'get' : 'doctor_details'
    }), name="doctor_details"),
    path("doctor/<str:doctor_id>/review/", doctor_api.DoctorReviewViewSet.as_view({
        'post' : 'create',
        'delete' : 'destroy',
        'get' : 'review_details'
    }), name="doctor_review"),
    path("doctor/<str:doctor_id>/pharmacy/", doctor_api.pharmacies_for_a_doctor, name="pharmacies_for_a_doctor"),


    ## pharmacy
    path("pharmacy/<str:pharmacy_id>/", pharmacy_api.PharmacyOverviewDetailsViewset.as_view({
        'get' : 'pharmacy_details'
    }), name="pharmacy_details"),
    path("pharmacy/<str:pharmacy_id>/review/", pharmacy_api.PharmacyReviewViewSet.as_view({
        'post' : 'create',
        'delete' : 'destroy',
        'get' : 'review_details'
    }), name="pharmacy_review"),
    path("pharmacy/<str:pharmacy_id>/doctor/", pharmacy_api.doctors_in_a_pharmacy, name="doctors_in_a_pharmacy"),

    ## appointment & schedule
    path("schedule/doctor/<str:doctor_id>/", appointment.doctor_schedules , name="doctor_schedules"),
    path("appointment/doctor/<str:doctor_id>/pharmacy/<str:pharmacy_id>/schedule/<str:schedule_id>/", appointment.book_appointment, name="book_appointment"),



] 
