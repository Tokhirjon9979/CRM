from django.db import models
from accounts.models import User


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    employees = models.ManyToManyField(User, related_name='employee')


    def __str__(self):
        return self.name
