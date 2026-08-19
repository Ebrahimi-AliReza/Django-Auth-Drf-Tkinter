
from rest_framework.response import Response
from ...models import User 
from rest_framework import status

from .serializers import RegistrationSerializer, LoginTokenSerializer
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken, Token



class SignupAPIView(GenericAPIView):
    permission_classes=[(AllowAny)]
    serializer_class=RegistrationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        data={
            'message':'User created successfully',
            'user':serializer.data
        }   
        return Response(data,status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    serializer_class = LoginTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'email':user.email,
                         'detail':'login is successful for you'},status=status.HTTP_202_ACCEPTED)
    