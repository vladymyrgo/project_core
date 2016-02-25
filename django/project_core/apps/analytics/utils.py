from core.utils.redis_utils import redis_client


def get_ab_test_case(request, ab_test_uid):
    a_b = request.session.get('ab_test')
    if a_b:
        r = redis_client()
        r.hincrby('analytics.ab_tests.uid_total_hits:{}'.format(ab_test_uid), '{}_hits'.format(a_b), 1)
    return a_b
