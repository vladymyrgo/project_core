from django.conf import settings
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

urlpatterns = [
    # url(r'^', include('my_new_app.urls', namespace='my_new_app')),
    url(r'^', include('account.urls.general', namespace='account')),
    url(r'^api/internal/', include('api_internal.urls', namespace='api_internal')),
    url(r'^api/v1/', include('project_core.urls._api_v1', namespace='api_v1')),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),
                    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                    ] + staticfiles_urlpatterns()
