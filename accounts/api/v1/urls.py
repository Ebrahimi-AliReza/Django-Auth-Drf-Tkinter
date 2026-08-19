from django.urls import path
from .views import *
#from rest_framework.authtoken.views import ObtainAuthToken
#for username authentication






urlpatterns = [
 path("signup/",SignupAPIView.as_view() , name="SignupAPIView"),
 #path("login/",ObtainAuthToken.as_view() , name="ObtainAuthToken"),
 path("login/",LoginView.as_view() , name="LoginView"),
   
 ]
