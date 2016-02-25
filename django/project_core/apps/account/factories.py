import factory


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Sequence(lambda n: "user_%d@mail.com" % n)
    password = factory.PostGenerationMethodCall('set_password',
                                                'default_password')

    class Meta:
        model = 'account.User'


class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True
