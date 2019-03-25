from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Announcement, AnnouncementImage, Category


class AnnouncementImageAdminInline(admin.TabularInline):
    model = AnnouncementImage


class AnnouncementAdmin(admin.ModelAdmin):
    inlines = (AnnouncementImageAdminInline, )


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Category, MPTTModelAdmin)
