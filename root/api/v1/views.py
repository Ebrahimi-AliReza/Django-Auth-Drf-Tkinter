from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InfoSerializers




@api_view()
def test(request):
    return Response({'name':'alireza',
                     'family':'ebrahimi'} )
    
    
    
@api_view(['POST','UPDATE'])
def test2(request):
    info={'name':'alireza',
                     'family':'ebrahimi'}
    serializer=InfoSerializers(info)
    return Response(serializer.data )