from django.conf.urls import url
from django.contrib.auth.views import logout

from account.views.general import SignUpView, LoginView


urlpatterns = [
    url(r'^sign-up/$', SignUpView.as_view(), name='sign_up'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout')
]
