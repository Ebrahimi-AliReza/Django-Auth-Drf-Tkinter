from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from services.models import Services,Category
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .serializers import ServicesSerializers
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from .permissions import IsAdminOrReadOnly
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet


class ServicesView(ModelViewSet):
    serializer_class=ServicesSerializers
    permission_classes=[AllowAny]
    queryset=Services.objects.all()

# class ServicesListView(ListAPIView, ListCreateAPIView):
#    serializer_class = ServicesSerializers
#    permission_classes = [AllowAny]#

#    def get_queryset(self):
#        return Services.objects.all()#

#    def get(self, request, *args, **kwargs):
#        return super().get(request, *args, **kwargs)#

#    def post(self, request, *args, **kwargs):
#        return super().post(request, *args, **kwargs)#


#class ServicesListView(GenericAPIView, ListModelMixin, CreateModelMixin):
#    serializer_class = ServicesSerializers
#    permission_classes = [AllowAny]#

#    def get_queryset(self):
#        return Services.objects.all()#

#    def get(self, request,*args, **kwargs):
#        return self.list(request, *args, **kwargs)#

#    def post(self, request,*args, **kwargs):
#        return self.create(request, *args, **kwargs)



# class ServiceListView(APIView):
#     def get_permissions(self):
#         if self.request.method=="GET":
#             return ([AllowAny()])
#         return([IsAdminUser()])
#     def get(self, *args, **kwargs):
#         services=Services.objects.all()
#         serializer=ServicesSerializers(services,many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK )
#     def post(self,request, *args, **kwargs):
#         serializer=ServicesSerializers(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'message':'data create successfully'}, status=status.HTTP_201_CREATED )
        
        
# class ServiceDetailView(APIView):
#     def get_permissions(self):
#         if self.request.method=="GET":
#             return ([AllowAny()])
#         return([IsAdminUser()])
    
#     def get_object(self,id):
#         service=get_object_or_404(Services,pk=id)
#         return service
    
       
#     def get(self,request,pk):
#         service=self.get_object(pk)
#         serializer=ServicesSerializers(service)
#         return Response(serializer.data , status=status.HTTP_200_OK )
    
#     def put(self,request,pk):
#         service=self.get_object(pk)
#         serializer=ServicesSerializers(Service, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'message':'data update successfully'}, status=status.HTTP_202_ACCEPTED)
        

#     def delete(self,request,pk):
#         service=self.get_object(pk)
#         service.delete()
#         return Response({'message':'data delete successfully'}, status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET',"POST"])
# @permission_classes([IsAdminOrReadOnly])
# def services(request):
#     if request.method == "GET":
#         services=Services.objects.all()
#         serializer=ServicesSerializers(services,many=True)
#         return Response(serializer.data , status=status.HTTP_200_OK )
#     elif request.method == "POST":
#         serializer=ServicesSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'data create successfully'}, status=status.HTTP_201_CREATED )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
        
        
            
            
# @api_view(['GET',"PUT",'DELETE'])
# @permission_classes([IsAdminOrReadOnly])
# def service_detail(request,pk):
#     service=get_object_or_404(Services,pk=pk)
#     if request.method == "GET":
#         serializer=ServicesSerializers(service)
#         return Response(serializer.data , status=status.HTTP_200_OK )
#     elif request.method == "PUT":
#         serializer=ServicesSerializers(Services,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message':'data updated successfully'}, status=status.HTTP_202_ACCEPTED )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         service.delete()
#         return Response({'message':'data delete successfully'}, status=status.HTTP_204_NO_CONTENT)
        
        
# class ServiceDetailView(GenericAPIView, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin):#

#    serializer_class = ServicesSerializers
#    permission_classes = [AllowAny]
#    queryset = Services.objects.filter(status=True)#

#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)#

#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)#

#    def delete(self, request, *args, **kwargs):
#        return self.destroy(request, *args, **kwargs)
   
   
class ServiceListView(ListCreateAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]


class ServiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializers

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]