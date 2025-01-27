from django.contrib import admin

from .models import Platform


# Register your models here.
@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'description',
        'logo',
    ]
