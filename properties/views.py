from django.shortcuts import render,get_object_or_404
from .models import Property


def properties(request):
    properties=Property.objects.all()
    context={'properties':properties}
    
    return render(request, 'properties/properties.html',context)

def property_single(request,id):
    property=get_object_or_404(Property,id=id)
    context={'property':property}
    return render(request, 'properties/property-single.html',context)

# Create your views here.

