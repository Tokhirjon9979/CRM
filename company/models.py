from django.db import models
from django.utils import timezone

from accounts.models import User
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('owner'))
    phone = models.CharField(max_length=20, verbose_name=_('phone'))
    logo = models.ImageField(upload_to='media/', blank=True, verbose_name=_('logo'))
    email = models.EmailField(max_length=255, unique=True, verbose_name=_('email'))
    employees = models.ManyToManyField(User, related_name='employees', verbose_name=_('employees'))

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    price = models.DecimalField(max_digits=50, decimal_places=0, verbose_name=_('price'))
    description = models.TextField(default='', blank=True, verbose_name=_('description'))
    image = models.ImageField(upload_to='media/', blank=True, verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('created_at'))
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))


    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.name
