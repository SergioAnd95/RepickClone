from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LikelistConfig(AppConfig):
    name = 'likelist'
    verbose_name = _('Список понравившегось')
