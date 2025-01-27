from django.contrib import admin

from .models import Token


# Register your models here.
@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'key',
        'created_at',
    ]
