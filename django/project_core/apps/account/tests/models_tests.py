from django.test import TestCase

from account.models import User

from account.factories import UserFactory


class UserTest(TestCase):

    def test_create_user(self):
        users_exists = User.objects.filter().exists()
        self.assertFalse(users_exists)

        UserFactory()
        users_exists = User.objects.filter().exists()
        self.assertTrue(users_exists)
