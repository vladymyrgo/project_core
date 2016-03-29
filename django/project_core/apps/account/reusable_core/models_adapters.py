from core.reusable_core.models_adapters import CoreModelAdapter


class UserAdapter(object):

    @property
    def prt_is_active(self):
        return self.is_active

    @property
    def prt_date_joined(self):
        return self.date_joined

    @property
    def prt_email(self):
        return self.email

    @property
    def prt_username(self):
        return self.username

    @property
    def prt_is_staff(self):
        return self.is_staff

    @property
    def prt_is_superuser(self):
        return self.is_superuser

    @property
    def prt_last_login(self):
        return self.last_login

    @property
    def prt_password(self):
        return self.password

    @classmethod
    def get_empty_queryset(cls):
        return cls.objects.none()

    @classmethod
    def get_actual_list_by_ids(cls, ids):
        return cls.objects.actual_list_by_ids(ids)


class UserPhotoAdapter(CoreModelAdapter):

    @property
    def prt_user(self):
        return self.user

    @property
    def prt_image(self):
        return self.image

    def delete_image(self):
        self.image.delete()
