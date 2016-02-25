# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third-party apps
    'django_jinja',
    'rest_framework',
    'haystack',

    # dev tools
    'django_extensions',
    'debug_toolbar',
    'django_nose',

    # project apps
    'account',
    'analytics',
    'api_internal',
    'core',
]
