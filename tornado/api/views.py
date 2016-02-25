from sockjs.tornado import SockJSConnection
from tornado import gen
from backends.redis.clients import redis_channels

from .commands import CommandHandler


class ApiHandler(CommandHandler, SockJSConnection):

    def on_open(self, info):
        self._subscriptions = set()

        try:
            sessionid = info.get_cookie('sessionid').value
        except (AttributeError, KeyError):
            sessionid = None
        if sessionid:
            self.cmd_auth(sessionid)

    def on_close(self):
        self._unsubscribe()

    @gen.coroutine
    def on_message(self, msg):
        pass

    def _subscribe(self, channel_name):
        if not isinstance(channel_name, list):
            channel_name = [channel_name]
        self._subscriptions |= set(channel_name)
        redis_channels().subscribe(channel_name, self)

    def _unsubscribe(self, channel_names=None):
        if not channel_names:
            channel_names = list(self._subscriptions)
        unsubscribe_from = [channel_name
                            for channel_name in channel_names
                            if channel_name in self._subscriptions]
        for channel_name in unsubscribe_from:
            redis_channels().unsubscribe(channel_name, self)
        self._subscriptions -= set(unsubscribe_from)
