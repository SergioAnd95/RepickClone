from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CatalogueConfig(AppConfig):
    name = 'catalogue'
    verbose_name = _('Каталог')
