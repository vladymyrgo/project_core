How to use AB tests

1) Set ANALYTICS_AB_TESTS_TURNED_ON in settings to True

2) Create in admin new ABTest instance. In description describe meaning of "test actions uid".

# Notes:
# abtu is AB test uid
# abau is AB test action uid

3) In a view do something like this:
    def get_template_names(self):
        # ab_test_uid is uid of ABTest
        a_b = get_ab_test_case(request=self.request, ab_test_uid='1_ab_t')
        if a_b == 'A':
            return 'page/some_page_A.jinja2'
        elif a_b == 'B':
            return 'page/some_page_B.jinja2'
        else:
            return 'page/some_page.jinja2'
4) In template add urls like:
    <a class="btn btn-primary" href="{{ url('some') }}?abtu=1_ab_t&abau=a_t" role="button">Get started</a>


Django ORM queries example for analytics:
DailyRequestsStatistics.objects.filter(json_data__contains={'/my-page': {'unique_visitors': u'1'}})
