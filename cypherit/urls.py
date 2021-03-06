"""cypherit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from core.views import CaeserCypherView,PA0View,KeyGeneratorView,EncryptImageView
from core.views import DecryptImageView,ImageIncreaseBrightness,ImageNegation,ImageBlur,ImageEdgeDetect, Des,DesAvalanche

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('caeser',CaeserCypherView.as_view(),name='CaeserCypher'),
    path('pa0',PA0View.as_view(),name="PA0"),
    path('generate-keys',KeyGeneratorView.as_view(),name="KeyGenerator0"),
    path('encrypt-image',EncryptImageView.as_view(),name="EncryptImage"),
    path('decrypt-image',DecryptImageView.as_view(),name="DecryptImage"),
    path('inc-brightness',ImageIncreaseBrightness.as_view(),name="ImageIncreaseBrightness"),
    path('image-negation',ImageNegation.as_view(),name="ImageNegation"),
    path('image-blur',ImageBlur.as_view(),name="ImageBlur"),
    path('image-edge-detect',ImageEdgeDetect.as_view(),name="ImageEdgeDetect"),
    path('des',Des.as_view(),name="DES"),
    path('des-avalanche',DesAvalanche.as_view(),name="DesAvalanche"),
]
