from django.conf import settings


def defaults(request):
    return {
        'settings': settings,
    }
