import json

from tornado.options import options

from tornadoredis import Client
from tornadoredis.pubsub import SockJSSubscriber
from redis import Redis
from backends.decorators import memoize


class JsonSockJSSubscriber(SockJSSubscriber):
    def on_message(self, msg):
        super(JsonSockJSSubscriber, self).on_message(msg)

        if msg.kind == 'message' and msg.body:
            # Get the list of subscribers for this channel
            subscribers = list(self.subscribers[msg.channel].keys())
            if subscribers:
                subscribers[0].broadcast(subscribers, json.loads(msg.body))


def async_client(host=None, port=None, db=None, io_loop=None):
    """
    Returns a new redis client instance.
    """
    options = _get_options(host, port, db)
    c = Client(**options)
    return c


@memoize
def redis_channels():
    return JsonSockJSSubscriber(async_client())


REDIS_CLIENT = None


def redis_client(host=None, port=None, db=None):
    """
    Returns a synchronous Redis client for 'simple' operations
    """
    global REDIS_CLIENT

    if not REDIS_CLIENT:
        REDIS_CLIENT = Redis(**_get_options(host, port, db=db, sync=True))
    return REDIS_CLIENT


def _get_options(host=None, port=None, db=None, sync=False):
    host = host or options.REDIS_HOST
    port = port or options.REDIS_PORT
    db = db or options.REDIS_DB
    res = {'host': host,
           'port': port,
           'db' if sync else 'selected_db': db}
    return res
