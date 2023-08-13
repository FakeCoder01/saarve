from rest_framework.decorators import permission_classes, api_view, authentication_classes
from doctor.models import Doctor, DoctorSchedule
from rest_framework import status
from rest_framework.response import Response
from .serializers import DoctorScheduleSerializer, AppointmentBookingSerializer, BookingSerializer, AppointmentSerializer
from django.db.models import F, DateTimeField, ExpressionWrapper, DurationField
from pharmacy.models import Pharmacy
from core.models import Appointment, Booking, Payment

@api_view(['GET'])
@permission_classes({})
@authentication_classes([])
def doctor_schedules(request, doctor_id):
    if not Doctor.objects.filter(id=doctor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    doctor = Doctor.objects.get(id=doctor_id)
  
    schedules = DoctorSchedule.objects.filter(doctor=doctor, start_time__date__gte='2023-08-13').annotate(
                    expected_appointment_time = ExpressionWrapper (
                        F('start_time') + 
                        ExpressionWrapper(
                            F('total_booked') * F('duration'),
                            output_field=DurationField(),
                        ),
                        output_field=DateTimeField(),
                    )
                )

    serializer = DoctorScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes({})
@authentication_classes([])
def book_appointment(request, doctor_id, pharmacy_id, schedule_id):

    if not Doctor.objects.filter(id=doctor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not Pharmacy.objects.filter(id=pharmacy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not DoctorSchedule.objects.filter(id=schedule_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    appointment_serializer = AppointmentSerializer(data=request.data)
    if not appointment_serializer.is_valid():
        return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    profile = request.user.user_profile
    appointment = appointment_serializer.save()
    
    booking_serializer = BookingSerializer(data=request.data)
    appointment_booking_serializer = AppointmentBookingSerializer(data=request.data)
    
    






"""
I have a list of dictionaries like this :

[
    {
        "date" : "string",
        "doctor" : "string",
        "pharmacy" : "string",
        "start_time" : "string",
        "end_time" : "string",
        "duration" : "integer",
        "total_booked" : "integer",
        "expected_appointment_time" : "string",
        "fees" : "float"
    },
    ...
]

And I want to convert it like this:

[
    {
        "date" : [
            {
                "doctor" : "string",
                "pharmacy" : "string",
                "start_time" : "string",
                "end_time" : "string",
                "duration" : "integer",
                "total_booked" : "integer",
                "expected_appointment_time" : "string",
                "fees" : "float"
            },
            ...
        ]
    },
    ...
]
"""