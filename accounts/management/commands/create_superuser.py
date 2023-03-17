import environ

from accounts.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

# from config.settings import env


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


class Command(BaseCommand):
    help = 'Generate random users'

    def handle(self, *args, **kwargs):
        username = env('SUPERUSER_USERNAME')
        email = env('SUPERUSER_EMAIL')
        password = env('SUPERUSER_PASSWORD')
        # print(username, email, password)

        try:
            user = User.objects.create_user(username=username, email=email, password=password, is_superuser=True, is_staff=True)
            user.save()
            self.stdout.write('Superuser created')
        except:
            self.stdout.write('Superuser not created')
