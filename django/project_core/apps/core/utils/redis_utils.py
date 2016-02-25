import json
import redis

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


def redis_client():
    """
    Returns Redis client.
    """
    redis_settings = settings.REDIS_SETTINGS
    return redis.Redis(host=redis_settings['HOST'],
                       port=redis_settings['PORT'],
                       db=redis_settings['DB_DATA'])


def redis_publish(event_channel, data):
    """
    Publishes the message to the Redis Pub/Sub channel.

    The data will be JSON-encoded.
    """
    return redis_client().publish(event_channel,
                                  json.dumps(data, cls=DjangoJSONEncoder))
