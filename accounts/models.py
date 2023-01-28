from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
import random
USERS_CHOICES = (
    ('admin', 'admin'),
    ('employee', 'employee'),
)

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=12, blank=True)
    photo = models.ImageField(null=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=8, choices=USERS_CHOICES, default='admin')

    def verify_email(self):
        self.verification_code = random.randint(1000, 9999)
        self.save()
        subject = 'Your verification code'
        message = f'{self.verification_code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email, ]
        send_mail(subject, message, email_from, recipient_list)
        print(self.verification_code)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
