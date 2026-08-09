from django.urls import path
from .views import *






urlpatterns = [
    path("last_services/", last_services, name="last_services"),
    path("categories/", categories, name="categories"),

]
