from django.contrib import admin
from django.contrib.auth.models import Group

from account.models import User, UserPhoto


class UserPhotoInline(admin.TabularInline):
    model = UserPhoto
    extra = 0
    raw_id_fields = ('image',)


class UserAdmin(admin.ModelAdmin):
    inlines = [UserPhotoInline, ]


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
