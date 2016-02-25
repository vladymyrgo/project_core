from django.conf.urls import url

from account.views.api_v1 import (AccountListView, AccountDetailView,
                                  AccountEditView, AccountSearchListView)


urlpatterns = [
    url(r'^$', AccountListView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', AccountDetailView.as_view(), name='detail'),
    url(r'^edit/$', AccountEditView.as_view(), name='detail'),
    url(r'^search/$', AccountSearchListView.as_view(), name='search'),
]
