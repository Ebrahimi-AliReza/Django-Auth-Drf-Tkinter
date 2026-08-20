
from django.contrib.auth.password_validation import ValidationError, validate_password
from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate    










class RegistrationSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True,required=True,style={'input_type':'password'})
 
    class Meta:
        model=User
        fields=['email','password','password1']
        
    def validate(self,attrs):
        if attrs.get('password')!=attrs.get('password1'):
            raise serializers.ValidationError({'password':'Password fields did not match'})
        try:
            validate_password(attrs.get('password'))
        except ValidationError as e:
            raise serializers.ValidationError({'password':list(e.messages)})
        return attrs
    def create(self,validated_data):
        validated_data.pop('password1')
        user=User.objects.create_user(**validated_data)
        return user             
    




class LoginTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        required=True,
        write_only=True
    )

    new_password = serializers.CharField(
        required=True,
        write_only=True
    )

    conf_password = serializers.CharField(
        required=True,
        write_only=True
    )


    def validate(self, attrs):

        if attrs['new_password'] != attrs['conf_password']:
            raise serializers.ValidationError({
                'conf_password': 'Passwords do not match.'
            })

        try:
            validate_password(attrs['new_password'])

        except ValidationError as e:
            raise serializers.ValidationError({
                'new_password': list(e.messages)
            })

        return attrs


    def validate_old_password(self, value):

        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                'Old password is incorrect.'
            )

        return value