from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PollConfig(AppConfig):
    name = 'poll'
    verbose_name = _('Poll')
