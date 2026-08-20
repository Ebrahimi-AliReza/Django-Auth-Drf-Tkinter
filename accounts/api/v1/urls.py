from django.urls import path
from .views import *
#from rest_framework.authtoken.views import ObtainAuthToken
#for username authentication






urlpatterns = [
 path("signup/",SignupAPIView.as_view() , name="SignupAPIView"),
 #path("login/",ObtainAuthToken.as_view() , name="ObtainAuthToken"),
 path("login/",LoginView.as_view() , name="LoginView"),
 path("logout/",LogoutView.as_view() , name="LogoutView"),
 path("change-password/",ChangePasswordView.as_view() , name="ChangePasswordView"),
   
 ]



#curl -X 'GET' 'http://127.0.0.1:8000/api/v1/services/'for curl request
# ----------------------------------------------------------------------------
# curl -X 'POST' \                                                         'http://127.0.0.1:8000/api/v1/accounts/login/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -H 'X-CSRFTOKEN: DX8MreQlCcJdeO5PE3eHHPpmenmwtFsvpkH6HKBm6x1n81INIGRqpdXGg7Rt0bzR' \
#   -d '{
#   "email": "admin@admin.com",
#   "password": "1234"
# }'
# ----------------------------------------------------------------------------
# curl -X 'GET' \
#   'http://127.0.0.1:8000/api/v1/services/' \
#   -H 'Content-Type: application/json' \
# > -H "Authorization:Token 4b9d317371233c322688ddb6535ff6c3d6e4a140"
# ----------------------------------------------------------------------------
# curl -X POST 'http://127.0.0.1:8000/api/v1/accounts/logout/' \
# -H 'Content-Type: application/json' \
# -H 'Authorization: Token 0b564ab44dca71cf16d84f84d6dd5593f23797ca'
