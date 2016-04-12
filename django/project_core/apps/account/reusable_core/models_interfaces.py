from core.reusable_core.models_interfaces import CoreInterface, CoreModelInterface


class UserInterface(CoreInterface):
    _required_attributes = [
        # properties:
        'prt_is_active',
        'prt_date_joined',
        'prt_email',
        'prt_username',
        'prt_is_staff',
        'prt_is_superuser',
        'prt_last_login',
        'prt_password',

        # methods:
        'is_authenticated',
        'get_short_name',
        'get_full_name',
    ]

    def __unicode__(self):
        raise NotImplementedError()

    @classmethod
    def get_empty_queryset(cls):
        raise NotImplementedError()

    @classmethod
    def get_actual_list_by_ids(cls, ids):
        raise NotImplementedError()


class UserPhotoInterface(CoreModelInterface):
    _required_attributes = [
        # properties:
        'prt_user',
        'prt_image',

        # methods:
        'delete',
        'delete_image',
    ]
