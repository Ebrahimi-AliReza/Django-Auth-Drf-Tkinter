
from django.urls import path
from .views import *



urlpatterns =[
    #('', services, name='services'),
    #path('', ServiceListView.as_view(), name='services'),
    path('', ServicesView.as_view({'get':'list','post':'create'}), name='services'),
    #path('detail/<int:pk>/', service_detail, name='service-detail'),
    #path('detail/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('detail/<int:pk>/', ServicesView.as_view({'put':'update','delete':'destroy','get':'retrieve'}), name='service-detail'),

]

