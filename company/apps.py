from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'company'
    verbose_name = _('company')

    # class ProductConfig(AppConfig):
    #     default_auto_field = 'django.db.models.BigAutoField'
    #     name = 'prooduct'
    #     verbose_name = _('product')

    def ready(self):
        import company.signals  # noqa
