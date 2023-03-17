from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.utils.translation import gettext_lazy as _

USERS_CHOICES = (
    ('admin', 'admin'),
    ('employee', 'employee'),
)


# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True, verbose_name=_('email'))
    first_name = models.CharField(max_length=150, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=150, blank=True, verbose_name=_('last name'))
    phone = models.CharField(max_length=12, blank=True, verbose_name=_('phone'))
    photo = models.ImageField(null=True, blank=True, verbose_name=_('photo'))
    email_verified = models.BooleanField(default=False, verbose_name=_('email verified'))
    verification_code = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('verification code'))
    type = models.CharField(max_length=8, choices=USERS_CHOICES, default='admin', verbose_name=_('type'))

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def send_email_code(self):
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
