from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField

from core.models.core_model import CoreModel


class DailyRequestsStatistics(CoreModel):
    json_data = JSONField()

    class Meta:
        app_label = 'analytics'
        verbose_name = "DailyRequestsStatistics"
        verbose_name_plural = "DailyRequestsStatistics"

    def __unicode__(self):
        return str(self.created.date())
