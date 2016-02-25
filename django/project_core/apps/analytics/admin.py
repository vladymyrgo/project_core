from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import ABTest, DailyABStatistics, DailyRequestsStatistics


class ABTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'uid',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('uid', 'json_description')
        return self.readonly_fields


class DailyABStatisticsAdmin(admin.ModelAdmin):
    list_display = ('title', 'ab_test',)
    list_filter = ('ab_test__title',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return obj._meta.get_all_field_names()

    def title(self, obj):
        return obj.created.date()
    title.short_description = _('created')


class DailyRequestsStatisticsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return obj._meta.get_all_field_names()


admin.site.register(ABTest, ABTestAdmin)
admin.site.register(DailyABStatistics, DailyABStatisticsAdmin)
admin.site.register(DailyRequestsStatistics, DailyRequestsStatisticsAdmin)
