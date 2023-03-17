from django.db import models

from accounts.models import User
from company.models import Company
from django.utils.translation import gettext_lazy as _

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    address = models.CharField(max_length=255, verbose_name=_('address'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_('company'))
    employee = models.ManyToManyField(User, related_name='employee', verbose_name=_('employee'))

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def __str__(self):
        return self.name


class LocationImages(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    location = models.ForeignKey(Location, on_delete=models.CASCADE, verbose_name=_('location'))
    image = models.ImageField(upload_to='media/', blank=True, verbose_name=_('image'))

    class Meta:
        verbose_name = _('LocationImage')
        verbose_name_plural = _('Location Images')

    def __str__(self):
        return self.title
