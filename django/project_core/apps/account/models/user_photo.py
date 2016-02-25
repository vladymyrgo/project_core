from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import CoreModel, CoreManager


class UserPhotoManager(CoreManager):
    pass


class UserPhoto(CoreModel):
    user = models.ForeignKey('account.User', verbose_name=_('User'), related_name='photos')
    image = models.OneToOneField('core.Image', verbose_name=_('User photo'), related_name='user_photo', on_delete=models.CASCADE)

    objects = UserPhotoManager()

    class Meta:
        app_label = 'account'
        verbose_name = "UserPhoto"
        verbose_name_plural = "UserPhotos"

    def __unicode__(self):
        return str(self.created.date())

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(UserPhoto, self).delete(*args, **kwargs)
