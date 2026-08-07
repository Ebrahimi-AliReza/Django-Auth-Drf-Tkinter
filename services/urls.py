from django.urls import path
from .views import *

app_name='services'

urlpatterns = [
    path('',ServicesView.as_view(),name='services'),
    path('tag/<str:tag>/',ServicesView.as_view(),name='services_by_tag'),
    path('category/<str:category>/',ServicesView.as_view(),name='services_by_category'),
    path('detail/<int:pk>/',ServiceDetailView.as_view(),name='detail')
]
