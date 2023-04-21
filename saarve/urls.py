"""saarve URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path
from . import csrf_google


urlpatterns = [
    path('admin/', admin.site.urls),    
    path('api/core/', include('core.urls'), name="core"),
    path('api/doctor/', include('doctor.urls'), name="doctor"),
    path('api/pharmacy/', include('pharmacy.urls'), name="pharmacy"),
    path('api/app/', include('app.urls'), name="app"),
    path('api/chat/', include('chat.urls'), name="chat"),

    
    path('cookie/csrf/', csrf_google.set_csrf_token, name="set_csrf_token"),
    path('auth/google/', csrf_google.google_login_access_token, name="google_login_access_token"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
