from django.conf import settings
from users.models import User, Client, Expert, Agent
from users.models import Profile
from users.serializers import ProfileModelSerializer

from django.core.validators import RegexValidator
from django.contrib.auth import password_validation, authenticate

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token

import jwt


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""
    
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""
        model = User
        fields = (
            'name',
            'last_name',
            'email',
            
        )

class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validation and user/profile creation.
    """
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
        
    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: +999999999. Up to 15 digits allowed."
    )
    phone_number = serializers.CharField(validators=[phone_regex])
    
    
    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)
    
    # Name
    name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    
    def validate(self, data):
        """Verify passwords match."""
        password = data['password']
        passwd_confirmation = data['password_confirmation']
        if password != passwd_confirmation:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data
    
    def create_client(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data,is_client=True)
        Profile.objects.create(user=user)
        return user
    
    def create_expert(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data,is_expert=True)
        Profile.objects.create(user=user)
        return user
    
    def create_client(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data,is_agent=True)
        Profile.objects.create(user=user)
        return user        
        
class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)
    
    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key



class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()