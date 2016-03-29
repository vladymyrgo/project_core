from core.reusable_core.models_interfaces import CoreModelInterface


class UserInterface(object):

    def __unicode__(self):
        raise NotImplementedError()

    def is_authenticated(self):
        raise NotImplementedError()

    @property
    def prt_is_active(self):
        raise NotImplementedError()

    @property
    def prt_date_joined(self):
        raise NotImplementedError()

    @property
    def prt_email(self):
        raise NotImplementedError()

    @property
    def prt_username(self):
        raise NotImplementedError()

    @property
    def prt_is_staff(self):
        raise NotImplementedError()

    @property
    def prt_is_superuser(self):
        raise NotImplementedError()

    @property
    def prt_last_login(self):
        raise NotImplementedError()

    @property
    def prt_password(self):
        raise NotImplementedError()

    def get_short_name(self):
        raise NotImplementedError()

    def get_full_name(self):
        raise NotImplementedError()

    @classmethod
    def get_empty_queryset(cls):
        raise NotImplementedError()

    @classmethod
    def get_actual_list_by_ids(cls, ids):
        raise NotImplementedError()


class UserPhotoInterface(CoreModelInterface):

    def delete(self):
        raise NotImplementedError()

    @property
    def prt_user(self):
        raise NotImplementedError()

    @property
    def prt_image(self):
        raise NotImplementedError()

    def delete_image(self):
        raise NotImplementedError()
