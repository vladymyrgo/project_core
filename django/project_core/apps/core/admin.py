from django.contrib import admin

from core.models import Image


class ImageAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Hide the model from admin home page.
        """
        return {}


admin.site.register(Image, ImageAdmin)
