from unittest import skip

from django_webtest import WebTest

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from account.factories import UserFactory


class LoginTestCase(WebTest):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.password = 'default_password'

    @skip("Home page is required")
    def test_login__wrong_password__form_error(self):
        form = self.app.get(reverse('account:login')).forms[0]
        form['username'] = self.user.email
        form['password'] = 'error'
        response = form.submit()

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.app.session)

    @skip("Home page is required")
    def test_login__proper_name_password__logged(self):
        self.assertNotIn('_auth_user_id', self.app.session)

        form = self.app.get(reverse('account:login')).forms[0]
        form['username'] = self.user.email
        form['password'] = self.password
        response = form.submit()

        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.app.session)

    def test_logout__redirect(self):
        self.client.login(username=self.user.email, password=self.password)

        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(reverse('account:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
