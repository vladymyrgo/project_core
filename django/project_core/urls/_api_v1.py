from django.conf.urls import url, include


urlpatterns = [
    url(r'^accounts/', include('account.urls.api_v1', namespace='account')),
]
