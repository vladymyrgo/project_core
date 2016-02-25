from sockjs.tornado import SockJSRouter

from .views import ApiHandler

sockjs_settings = {
    'sockjs_url': 'https://cdn.jsdelivr.net/sockjs/1.0.3/sockjs.min.js',
}

urlpatterns = (SockJSRouter(ApiHandler, '/rt', sockjs_settings).urls)
