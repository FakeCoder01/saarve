from rest_framework.decorators import permission_classes, api_view, authentication_classes
from doctor.models import Doctor, DoctorSchedule
from rest_framework import status
from rest_framework.response import Response
from .serializers import DoctorScheduleSerializer, AppointmentBookingSerializer, AppointmentSerializer
from django.db.models import F, DateTimeField, ExpressionWrapper, DurationField
from core.models import  Booking, Payment
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication, TokenAuthentication




@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def doctor_schedules(request, doctor_id):
    if not Doctor.objects.filter(id=doctor_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    doctor = Doctor.objects.get(id=doctor_id)
  
    schedules = DoctorSchedule.objects.filter(doctor=doctor, start_time__date__gte='2023-08-13').annotate(
                    expected_appointment_time = ExpressionWrapper (
                        F('start_time') + 
                        ExpressionWrapper(
                            F('total_booked') * F('duration') * 1000000 * 60,
                            output_field=DurationField(),
                        ),
                        output_field=DateTimeField(),
                    )
                )

    serializer = DoctorScheduleSerializer(schedules, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_appointment(request, doctor_id, pharmacy_id, schedule_id):

    if not DoctorSchedule.objects.filter(id=schedule_id, doctor__id=doctor_id, pharmacy__id=pharmacy_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    appointment_serializer = AppointmentSerializer(data=request.data)
    if not appointment_serializer.is_valid():
        return Response(appointment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    schedule = DoctorSchedule.objects.get(id=schedule_id, doctor__id=doctor_id, pharmacy__id=pharmacy_id)
    avl_appointment_time = schedule.start_time + timedelta(minutes=schedule.total_booked * schedule.total_booked)

    print("Got : ", appointment_serializer.validated_data.get('appointment_date_time', None), " Required : ", avl_appointment_time)
    if appointment_serializer.validated_data.get('appointment_date_time', None) != avl_appointment_time:
        return Response({"detail" : "datetime mismatch"}, status=status.HTTP_400_BAD_REQUEST)

    appointment = appointment_serializer.save(schedule=schedule, no_in_queuee=schedule.total_booked + 1)
    payment = Payment.objects.create(amount=schedule.fees)

    profile = request.user.user_profile

    booking = Booking.objects.create(
        patient = profile,
        doctor = schedule.doctor,
        pharmacy = schedule.pharmacy,
        payment = payment,
        appointment = appointment
    )
    appointment_booking_serializer = AppointmentBookingSerializer(booking)
    return Response(appointment_booking_serializer.data, status=status.HTTP_201_CREATED)






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