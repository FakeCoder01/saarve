from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import PharmacyProfileSerializer, RegisterSerializer, OTPVerificationSerializer
from .models import PharmacyUser, Pharmacy
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from rest_framework import generics
from django.middleware.csrf import get_token

import random
# Create your views here.


class PharmacyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PharmacyProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Pharmacy.objects.get(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def profile_details(self, request, id=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=201)
        return Response({"detail" : "All fields are neccessary"}, status=413)
    

    def update(self, request, id=None):
        queryset = Pharmacy.objects.filter(user=self.request.user)
        pharmacy = get_object_or_404(queryset, user=request.user)
        serializer = self.get_serializer(pharmacy, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, id=None):
        if id == None:
            id = request.data.get('id')
        queryset = Pharmacy.objects.filter(user=self.request.user)
        pharmacy = get_object_or_404(queryset, id=id)
        pharmacy.delete()
        return Response(status=204)
    


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def set_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token':csrf_token})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def sign_up_register(request):
    serializer = RegisterSerializer(data=request.data)
    if request.data.get('confirm_password') != request.data.get('password'):
        return Response({'message': 'password not match'}, status=405)
    if serializer.is_valid():
        user = User.objects.create_user(
            username = request.data.get('username'),
            password = request.data.get('password'),
            email = request.data.get('email'),
            is_active = False
        )
        phrmacy_user = PharmacyUser.objects.create(
            user = user,
            name = request.data.get('name'),
            phone_number = request.data.get('phone_number'),
            pharmacy_reg_no = request.data.get('phramacy_reg_no'),
        )
        Group.objects.get(name='Pharmacies').user_set.add(user)
        email_code = random.randint(100000, 999999)
        phone_code = random.randint(100000, 999999)

        phrmacy_user.set_email_otp(str(email_code))
        phrmacy_user.set_phone_otp(str(phone_code))
        phrmacy_user.save()

        print("Email : ", email_code)
        print("Phone : ", phone_code)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token' : token.key, 'message': 'otp sent', 'next' : 'verify'}, status=200)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def otp_verification(request):
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        email_otp = request.data.get('email_otp')
        phone_otp = request.data.get('phone_otp')

        if not User.objects.filter(email=request.data.get('email'), is_active=False).exists() or not PharmacyUser.objects.filter(phone_number=request.data.get('phone_number')).exists():
            return Response({'detail' : 'error'}, status=403)
        user = PharmacyUser.objects.get(phone_number=request.data.get('phone_number'), user=User.objects.get(email=request.data.get('email'), is_active=False))
        if not user.verify_phone(str(phone_otp)):
            return Response({'detail' : 'otp mismatch0'}, status=402)
        if not user.verify_email(str(email_otp)):
            return Response({'detail' : 'otp mismatch1'}, status=402)
        user.save()
        return Response({'detail' : 'verification successful'}, status=200)
    return Response(serializer.errors, status=400)





@api_view(['POST', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def account_update_and_delete(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
    