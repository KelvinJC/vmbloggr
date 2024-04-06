from django.contrib import auth
from rest_framework import serializers, validators
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class UserSerializer(serializers.ModelSerializer):
    "Serialiser for all HTTP methods related to the user except POST."
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number'] 


class UserCreateSerializer(serializers.ModelSerializer):
    "Serialiser specific to creating a new user i.e. HTTP POST method."

    username = serializers.CharField(max_length=20, min_length=6)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'phone_number']
        extra_kwargs = {
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that email already exists."
                    )
                ]
            },
            "phone_number": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that phone number already exists."
                    )
                ]
            },
            "username": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that username already exists."
                    ),
                ]
            },   
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(self.default_error_messages)
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.ModelSerializer):
    ''' Serialiser to handle the login endpoint.'''
    password = serializers.CharField(max_length=68, min_length=6,write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['password', 'username', 'tokens']

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }
    
    def validate(self, attrs):
        username = attrs.get('username','')
        password = attrs.get('password','')
        user = auth.authenticate(
            username=username,
            password=password
        )

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again.')
        if not user.is_active:
            raise AuthenticationFailed('User disabled, contact admin.')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


