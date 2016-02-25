from django.conf.urls import url

from views import ApiAuthView


urlpatterns = [
    url(r'^auth/$', ApiAuthView.as_view(), name='auth'),
]
