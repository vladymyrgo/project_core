from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(UserManager):
    def actual_list(self):
        return self.get_queryset().filter(is_active=True)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_active = models.BooleanField(_('Active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    email = models.EmailField(_('Email'), max_length=255, db_index=True, unique=True)

    username = models.CharField(_('Username'), max_length=255, db_index=True, unique=True)

    is_staff = models.BooleanField(_('Staff status'), default=False)

    objects = UserManager()

    class Meta:
        app_label = 'account'
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __unicode__(self):
        return self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.username
