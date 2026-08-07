from django.contrib import admin
from .models import property_type, Status, Property
admin.site.register(property_type)
admin.site.register(Status)
admin.site.register(Property)

# Register your models here.
