from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

from core.models.core_model import CoreModel, CoreManager


class ABTestManager(CoreManager):
    pass


class ABTest(CoreModel):
    uid = models.CharField(_('uid'), max_length=255, db_index=True, unique=True)
    title = models.CharField(_('Title'), max_length=255)
    json_description = JSONField(_('Description'))

    objects = ABTestManager()

    class Meta:
        app_label = 'analytics'
        verbose_name = "ABTest"
        verbose_name_plural = "ABTests"

    def __unicode__(self):
        return self.title


class DailyABStatistics(CoreModel):
    ab_test = models.ForeignKey(ABTest, verbose_name=_('AB test'), related_name='daily_ab_statistics')
    json_data = JSONField(_('Data'))

    class Meta:
        app_label = 'analytics'
        verbose_name = "DailyABStatistics"
        verbose_name_plural = "DailyABStatistics"

    def __unicode__(self):
        return str(self.created.date())
