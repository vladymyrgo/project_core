from django.conf import settings

from core.utils.redis_utils import redis_client


class RequestStatisticsMiddleware(object):
    """
    Middleware that saves request statistics to Redis.
    """

    def process_response(self, request, response):
        ip = request.META.get('REMOTE_ADDR')
        path = request.path
        if settings.ANALYTICS_REQUESTS_TURNED_ON and \
                (str(response.status_code) not in settings.ANALYTICS_IGNORE_RESPONSE_STATUSES) and \
                (ip not in settings.ANALYTICS_IGNORE_IP) and \
                (path not in settings.ANALYTICS_IGNORE_PATH):
            r = redis_client()
            path_key = 'analytics.requests_statistics.path:{}'.format(path)
            r.hincrby(path_key, 'hits', 1)
            if r.sadd('analytics.requests_statistics.path_ip_set:{}'.format(path), ip):
                r.hincrby(path_key, 'unique_visitors', 1)

        return response


class ABStatisticsSession(object):
    """
    Middleware that sets A/B case to session.
    """

    def process_request(self, request):
        if settings.ANALYTICS_AB_TESTS_TURNED_ON:
            if 'ab_test' not in request.session:
                a_b = 'B' if settings.ANALYTICS_AB_TESTS_PREVIOUS_A else 'A'
                request.session.update({'ab_test': a_b})
                settings.ANALYTICS_AB_TESTS_PREVIOUS_A = not settings.ANALYTICS_AB_TESTS_PREVIOUS_A


class ABStatisticsSaveData(object):
    """
    Middleware that saves A/B statistics to Redis.
    """

    def process_request(self, request):
        if settings.ANALYTICS_AB_TESTS_TURNED_ON:
            ab_test_uid = request.GET.get('abtu')
            ab_test_action_id = request.GET.get('abau')
            if ab_test_uid and ab_test_action_id:
                r = redis_client()
                r.hincrby('analytics.ab_tests.uid:{}'.format(ab_test_uid), ab_test_action_id, 1)
