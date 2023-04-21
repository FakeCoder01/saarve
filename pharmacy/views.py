from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import viewsets
from .serializers import PharmacyProfileSerializer
from .models import Pharmacy
from django.shortcuts import get_object_or_404




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
        if id == None:
            id = request.data.get('id')
        queryset = Pharmacy.objects.filter(user=self.request.user)
        pharmacy = get_object_or_404(queryset, id=id)
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
    
