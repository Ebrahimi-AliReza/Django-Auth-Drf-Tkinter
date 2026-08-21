from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)
from django.utils.encoding import force_bytes

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from .serializers import (
    RegistrationSerializer,
    LoginTokenSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


User = get_user_model()



class SignupAPIView(GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()


        return Response(
            {
                "message":"User created successfully",
                "user":serializer.data
            },
            status=status.HTTP_201_CREATED
        )





class LoginView(ObtainAuthToken):

    serializer_class = LoginTokenSerializer


    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={
                "request":request
            }
        )


        serializer.is_valid(
            raise_exception=True
        )


        user = serializer.validated_data["user"]


        token, created = Token.objects.get_or_create(
            user=user
        )


        return Response(
            {
                "token":token.key,
                "email":user.email,
                "detail":"login successful"
            },
            status=status.HTTP_200_OK
        )





class LogoutView(GenericAPIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        if hasattr(request.user,"auth_token"):

            request.user.auth_token.delete()


        return Response(
            {
                "message":"Logout successful"
            },
            status=status.HTTP_200_OK
        )





class ChangePasswordView(GenericAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = ChangePasswordSerializer



    def post(self, request):

        serializer = self.get_serializer(
            data=request.data,
            context={
                "request":request
            }
        )


        serializer.is_valid(
            raise_exception=True
        )


        request.user.set_password(
            serializer.validated_data["new_password"]
        )


        request.user.save()


        return Response(
            {
                "message":"Password changed successfully"
            },
            status=status.HTTP_200_OK
        )







class PasswordResetRequestView(APIView):

    permission_classes = [AllowAny]


    def post(self, request):

        serializer = PasswordResetRequestSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        email = serializer.validated_data["email"]


        try:
            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":"User not found"
                },
                status=404
            )


        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )


        token = default_token_generator.make_token(
            user
        )


        link = (
            f"http://127.0.0.1:8000/"
            f"api/v1/accounts/"
            f"reset-confirm/"
            f"{uid}/"
            f"{token}/"
        )


        print("="*50)
        print("RESET PASSWORD LINK:")
        print(link)
        print("="*50)


        return Response(
            {
                "message":"Reset link generated",
                "link":link,
                "uid":uid,
                "token":token
            },
            status=200
        )




class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]


    def post(self, request, uid, token):

        serializer = PasswordResetConfirmSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        try:

            uid = urlsafe_base64_decode(
                uid + "=" * (-len(uid) % 4)
            ).decode()


            user = User.objects.get(
                pk=uid
            )


        except Exception:

            return Response(
                {
                    "error":"Invalid reset link"
                },
                status=400
            )



        if not default_token_generator.check_token(
            user,
            token
        ):

            return Response(
                {
                    "error":"Expired token"
                },
                status=400
            )


        user.set_password(
            serializer.validated_data["password"]
        )

        user.save()


        return Response(
            {
                "message":
                "Password changed successfully"
            },
            status=200
        )
        
        
class ProfileView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        serializer = UserProfileSerializer(
            request.user
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )