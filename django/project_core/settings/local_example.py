from . import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1sc=&tosn_-f%9v$zbp4fdi6!&*_m&2h1_7yh5q*8rb=p@o)f!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

NGINX = False

ALLOWED_HOSTS = ['127.0.0.1']


ADMINS = [
    # ['Your Name', 'your_email@example.com'],
]


# !!! MAILS !!!
# Send mails to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@mail.com'

# Send real mails
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.mail.ru'
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = 'robo@project_core.net'
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True
# SERVER_EMAIL = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# !!! END MAILS #!!!


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Analytics settings
ANALYTICS_AB_TESTS_TURNED_ON = False  # Postgres 9.4 or higher is required
ANALYTICS_REQUESTS_TURNED_ON = False  # Postgres 9.4 or higher is required
ANALYTICS_PERIODICITY_SAVE_TO_DB = 60  # minutes
ANALYTICS_IGNORE_RESPONSE_STATUSES = ['302', ]
ANALYTICS_IGNORE_IP = ['127.0.0.1', ]
ANALYTICS_IGNORE_PATH = []
ANALYTICS_AB_TESTS_PREVIOUS_A = True  # Technical value. Don't touch!


if 'test' in sys.argv:
    DEBUG = False
    TEMPLATE_DEBUG = False

    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    }

    MIGRATION_MODULES = {}
