import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from django.utils.timezone import now
from django.conf import settings

from core.utils.redis_utils import redis_client, redis_publish

from .models import ABTest, DailyABStatistics, DailyRequestsStatistics


@periodic_task(run_every=datetime.timedelta(minutes=settings.ANALYTICS_PERIODICITY_SAVE_TO_DB))
def task_save_redis_requests_statistics_to_db(statistics_date=None):
    """
    Task that saves redis requests statistics data to DB. Doesn't remove data in Redis.
    """
    if settings.ANALYTICS_REQUESTS_TURNED_ON:
        statistics_date = statistics_date or now().date()
        daily_requests_statistics = (DailyRequestsStatistics.objects
                                                            .filter(created__date=statistics_date)
                                                            .first())
        r = redis_client()
        redis_path_key_pattern = 'analytics.requests_statistics.path:'
        paths_keys = r.keys(redis_path_key_pattern + '*')
        json_data = {}
        for path_key in paths_keys:
            path = path_key.split(redis_path_key_pattern)[1]
            path_data = r.hgetall(path_key)
            json_data.update({path: {'hits': path_data.get('hits'),
                                     'unique_visitors': path_data.get('unique_visitors')
                                     }
                              })
        if daily_requests_statistics:
            (DailyRequestsStatistics.objects
                                    .filter(id=daily_requests_statistics.id)
                                    .update(json_data=json_data))
        else:
            DailyRequestsStatistics.objects.create(json_data=json_data)

        redis_publish('admin.notifications',
                      {'is_browser_notification': True,
                       'title': 'Admin notification',
                       'message': 'Request statistics was updated'})


@periodic_task(run_every=crontab(hour=00, minute=00))
def task_save_redis_requests_statistics_to_db_at_end_of_day():
    """
    Daily task that saves data to DB and remove all requests statistics data from Redis.
    """
    if settings.ANALYTICS_REQUESTS_TURNED_ON:
        previous_date = now().date() - datetime.timedelta(days=1)
        task_save_redis_requests_statistics_to_db(statistics_date=previous_date)

        r = redis_client()
        paths_keys = r.keys('analytics.requests_statistics.*')
        if paths_keys:
            r.delete(*paths_keys)


@periodic_task(run_every=datetime.timedelta(minutes=settings.ANALYTICS_PERIODICITY_SAVE_TO_DB))
def task_save_redis_ab_statistics_to_db(statistics_date=None):
    """
    Task that saves redis AB statistics data to DB. Doesn't remove data in Redis.
    """
    if settings.ANALYTICS_AB_TESTS_TURNED_ON:
        statistics_date = statistics_date or now().date()
        r = redis_client()
        redis_ab_tests_key_pattern = 'analytics.ab_tests.uid_total_hits:'
        ab_tests_keys = r.keys(redis_ab_tests_key_pattern + '*')
        for ab_test_key in ab_tests_keys:
            ab_test_uid = ab_test_key.split(redis_ab_tests_key_pattern)[1]
            ab_test = ABTest.objects.actual_list().filter(uid=ab_test_uid).first()

            if ab_test:
                daily_ab_statistics = (DailyABStatistics.objects
                                                        .filter(ab_test=ab_test,
                                                                created__date=statistics_date)
                                                        .first())

                ab_test_data = r.hgetall('analytics.ab_tests.uid:{}'.format(ab_test_uid))
                for key in ab_test_data.keys():
                    if key not in ab_test.json_description:
                        del ab_test_data[key]

                ab_test_data_hits = r.hgetall(ab_test_key)

                if ab_test_data_hits:
                    ab_test_data.update(ab_test_data_hits)

                if daily_ab_statistics:
                    (DailyABStatistics.objects
                                      .filter(id=daily_ab_statistics.id)
                                      .update(json_data=ab_test_data))
                else:
                    ab_test.daily_ab_statistics.create(json_data=ab_test_data)

        redis_publish('admin.notifications',
                      {'is_browser_notification': True,
                       'title': 'Admin notification',
                       'message': 'AB statistics was updated'})


@periodic_task(run_every=crontab(hour=00, minute=00))
def task_save_redis_ab_statistics_to_db_at_end_of_day():
    """
    Daily task that saves data to DB and remove all ab statistics data from Redis.
    """
    if settings.ANALYTICS_AB_TESTS_TURNED_ON:
        previous_date = now().date() - datetime.timedelta(days=1)
        task_save_redis_ab_statistics_to_db(statistics_date=previous_date)

        r = redis_client()
        paths_keys = r.keys('analytics.ab_tests.*')
        if paths_keys:
            r.delete(*paths_keys)
