from accounts.models import User
from django.core.management.base import BaseCommand
from company.models import Company
from location.models import Location, LocationImages


class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        parser.add_argument('username', type=int, help='Indicates the number of users to be created')
        parser.add_argument('company', type=int, help='Indicates the number of users to be created')
        parser.add_argument('location', type=int, help='Indicates the number of users to be created')
        parser.add_argument('location_images', type=int, help='Indicates the number of users to be created')
        parser.add_argument('employee', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        company = kwargs['company']
        location = kwargs['location']
        location_images = kwargs['location_images']
        employee = kwargs['employee']

        User.objects.bulk_create([User(username=f'testuser{i + 1}',
                                       email=f'testuser{i + 1}@gmail.com',
                                       password=f'testuser{i + 1}',
                                       type='admin') for i in range(username)])
        print('User created')

        companies = Company.objects.bulk_create([Company(name=f'testusercompany{j + 1}',
                                                         email=f'testusercompany{j + 1}@gmail.com',
                                                         owner=User.objects.get(username=f'testuser{j // company + 1}'))
                                                 for j in
                                                 range(company * username)])
        print('Company created')

        n = 1
        for companyy in companies:
            employes = User.objects.bulk_create([User(username=f'testemployee{n}{i + 1}',
                                                      email=f'testemployee{n}{i + 1}@gmail.com',
                                                      password=f'testemployee{n}{i + 1}',
                                                      type='employee',
                                                      ) for i in
                                                 range(employee)])
            companyy.employees.add(*employes)
            n += 1
        print('Employee created')

        Location.objects.bulk_create([Location(name=f'location_name{i + 1}',
                                               address=f'location_adress{i + 1}',
                                               company=Company.objects.get(name=f'testusercompany{i // location + 1}'))
                                      for i in
                                      range(company * location)])
        print('Location created')

        LocationImages.objects.bulk_create([LocationImages(title=f'locationtitle{i + 1}',
                                                           image=f'imagelocation{i + 1}',
                                                           location=Location.objects.get(
                                                               name=f'location_name{i // location_images + 1}')) for i
                                            in range(location * location_images)])
        print('Location images created')
