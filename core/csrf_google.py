from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from django.middleware.csrf import get_token



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def set_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrf_token':csrf_token})


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def google_login_access_token(request):
    token = request.data.get('id_token')
    usertype = request.data.get('usertype')

    if not token or not usertype:
        return Response({'error': 'Invalid request'}, status=400)
    try:
        idinfo = id_token.verify_oauth2_token(token, Request())
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_email = idinfo['email']
    except ValueError:
        return Response({'error': 'Invalid token'}, status=400)
    
    try:
        if not User.objects.filter(email=user_email).exists():
            user = User.objects.create(email=user_email, username=user_email)
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=400)
    
    match usertype:
        case "doctor":
            Group.objects.get("Doctors").user_set.add(user)
        case "user":
            Group.objects.get("Consumers").user_set.add(user)
        
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=200)

