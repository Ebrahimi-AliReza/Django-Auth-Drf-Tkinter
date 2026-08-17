from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from services.models import Services,Category
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from services.api.v1.serializers import ServicesSerializers,CategorySerializers




@api_view()
def last_services(request):
    last_three_service=Services.objects.all().order_by('-created_at')[:3]
    serializer=ServicesSerializers(last_three_service , many=True)
    return Response(serializer.data , status=status.HTTP_200_OK )
    
    
 
@api_view()
@permission_classes([IsAdminUser])  
def categories(request):
    categories=Category.objects.all()
    serializer=CategorySerializers(categories , many=True)
    return Response(serializer.data , status=status.HTTP_200_OK )