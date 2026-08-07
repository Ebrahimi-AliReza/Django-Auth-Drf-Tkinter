from django.urls import path
from .views import *
from django.views.generic import RedirectView



app_name = "root"

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", contact, name='contact'),
    path("agents/", agents, name="agents"),
    #path("soft98/",RedirectView.as_view(url='https://www.soft98.ir') , name="soft98"),
    path("soft98/",Soft98.as_view() , name="soft98"),
]
