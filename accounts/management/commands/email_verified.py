from accounts.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Email verified'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Enter your email')

    def handle(self, *args, **kwargs):
        email = kwargs['email']
        if email not in User.objects.values_list('email', flat=True):
            self.stdout.write('Please check your email')
        else:
            user = User.objects.get(email=email)

            if user.email_verified:
                self.stdout.write('Your email already verified')

            else:
                user.email_verified = True
                user.save()
                self.stdout.write('User email verified')

