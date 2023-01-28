from company.models import Company
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from accounts.validator_functions import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['password', 'username', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class VerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class VerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['verification_code']


class ForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20)
    password2 = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['email', 'verification_code', 'password', 'password2']


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone')

    def validate(self, attrs):
        valid_email(attrs.get('email'))
        valid_username(attrs.get('username'))
        valid_first_last_name(attrs.get('first_name'))
        valid_first_last_name(attrs.get('last_name'))
        valid_phone_number(attrs.get('phone'))
        return attrs


class AddEmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    company_id = serializers.CharField(max_length=10, min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'company_id', 'password', 'password2']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        phone = attrs.get('phone')

        valid_phone_number(phone)
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm password does not match')
        return attrs

    def create(self, validated_data):
        employee = User.objects.create_user(**validated_data)
        password = validated_data.get('password')
        employee.set_password(password)
        company_id = validated_data.get('company_id')

        employee.type = 'employee'
        employee.save()
        return employee
