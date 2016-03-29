from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.utils.utils import handle_filename

from core.reusable_core.models_adapters import ImageAdapter
from core.reusable_core.models_interfaces import ImageInterface

from core.models import CoreModel, CoreManager


class ImageManager(CoreManager):
    pass


class Image(CoreModel, ImageAdapter, ImageInterface):
    img = models.ImageField(_('image'), upload_to=handle_filename)

    objects = ImageManager()

    class Meta:
        app_label = 'core'
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __unicode__(self):
        return 'image'

    def delete(self, *args, **kwargs):
        self.delete_img()
        super(Image, self).delete(*args, **kwargs)
