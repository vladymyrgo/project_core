import os
import sys

from kombu import Exchange, Queue


# Project name
PROJECT_NAME = 'project_core'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'apps'),)


AUTH_USER_MODEL = 'account.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'analytics.middleware.RequestStatisticsMiddleware',
    'analytics.middleware.ABStatisticsSession',
    'analytics.middleware.ABStatisticsSaveData',
]

ROOT_URLCONF = PROJECT_NAME + '.urls.urls'

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [os.path.join(BASE_DIR, 'templates'), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".jinja2",
            "context_processors": [
                "core.context_processors.defaults",
            ],
        }
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates'), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.defaults",
            ],
        }
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

DESIGN_DIR = os.path.join(BASE_DIR, '..', '..', 'design')

STATICFILES_DIRS = [
    os.path.join(DESIGN_DIR, "app"),
]

PUBLIC_DIR = os.path.join(BASE_DIR, '..', '..', 'public')

STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PUBLIC_DIR, 'media')

# Tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Redis
REDIS_SETTINGS = {
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'DB_DATA': 5,
    'DB_CACHES': 6,
    'DB_CELERY_BROKER': 7,
    'DB_CELERY_RESULT': 7,
}


# Django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/{}".format(REDIS_SETTINGS['HOST'],
                                              REDIS_SETTINGS['PORT'],
                                              REDIS_SETTINGS['DB_CACHES']),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Celery
BROKER_URL = 'redis://{}:{}/{}'.format(REDIS_SETTINGS['HOST'],
                                       REDIS_SETTINGS['PORT'],
                                       REDIS_SETTINGS['DB_CELERY_BROKER'])

CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_IGNORE_RESULT = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_EVENT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://localhost:6379/{}'.format(REDIS_SETTINGS['DB_CELERY_RESULT'])
CELERY_DEFAULT_ROUTING_KEY = PROJECT_NAME
CELERYBEAT_SCHEDULE_FILENAME = '/tmp/{}-celerybeat-schedule'.format(PROJECT_NAME)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default')),
    Queue('long_tasks', Exchange('long_tasks')),
)


# Haystack / Elasticsearch
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
