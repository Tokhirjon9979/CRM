from django.core.validators import validate_email
from rest_framework import serializers


def valid_email(email):
    try:
        validate_email(email)
        return True
    except:
        raise serializers.ValidationError('Invalid email')


def valid_username(username):
    if not username.isalnum():
        raise serializers.ValidationError('Invalid username')
    return True


def valid_first_last_name(name):
    if not name.isalpha():
        raise serializers.ValidationError('Check your first name or last name')
    return True


def valid_phone_number(phone):
    if not phone.isnumeric() or len(phone) > 12:
        raise serializers.ValidationError('Your phone number has not numeric symbols or it is short')
    return True

