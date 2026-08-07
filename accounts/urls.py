from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('login/', Login_view.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('change-password/',change_password,name='change_pass'),
    path('reset-password/',reset_password,name='reset-password'),
    path('reset-password-done/',reset_password_done,name='reset-password-done'),
    path('reset-password-confirm/<str:token>',reset_password_confirm,name='reset-password-confirm'),
    path('reset-password-complete/',reset_password_complete,name='reset-password-complete'),
]

 