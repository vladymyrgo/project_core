from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

from core.reusable_core.models_adapters import CoreModelAdapter
from core.reusable_core.models_interfaces import CoreModelInterface


class CoreManager(models.Manager):
    def actual_list(self):
        return self.get_queryset().filter(is_active=True)


class CoreModel(models.Model, CoreModelAdapter, CoreModelInterface):
    is_active = models.BooleanField(_('Active'), default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'core'
        abstract = True
