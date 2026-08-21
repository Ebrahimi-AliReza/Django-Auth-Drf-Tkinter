from rest_framework import serializers
from accounts.models import User

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone',
            'password',
            'password1'
        ]

    def validate(self, attrs):

        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError(
                {
                    "password": "Password fields did not match"
                }
            )

        try:
            validate_password(attrs.get('password'))

        except ValidationError as e:
            raise serializers.ValidationError(
                {
                    "password": list(e.messages)
                }
            )

        return attrs


    def create(self, validated_data):

        validated_data.pop('password1')

        user = User.objects.create_user(
            **validated_data
        )

        return user



class LoginTokenSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )


    def validate(self, attrs):

        username = attrs.get("username")
        password = attrs.get("password")


        user = authenticate(
            username=username,
            password=password
        )


        if not user:
            raise serializers.ValidationError(
                "Invalid username or password"
            )


        attrs["user"] = user

        return attrs




class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        write_only=True
    )

    new_password = serializers.CharField(
        write_only=True
    )

    conf_password = serializers.CharField(
        write_only=True
    )


    def validate(self, attrs):

        if attrs["new_password"] != attrs["conf_password"]:
            raise serializers.ValidationError(
                {
                    "password":
                    "Passwords do not match"
                }
            )


        try:
            validate_password(
                attrs["new_password"]
            )

        except ValidationError as e:

            raise serializers.ValidationError(
                {
                    "password":list(e.messages)
                }
            )


        return attrs



    def validate_old_password(self,value):

        user = self.context['request'].user


        if not user.check_password(value):

            raise serializers.ValidationError(
                "Old password incorrect"
            )


        return value




class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "phone"
        ]




class PasswordResetRequestSerializer(serializers.Serializer):

    email = serializers.EmailField()




class PasswordResetConfirmSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
        min_length=6
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=6
    )


    def validate(self,data):

        if data["password"] != data["confirm_password"]:

            raise serializers.ValidationError(
                "Passwords do not match"
            )


        return data