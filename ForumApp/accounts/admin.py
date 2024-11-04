from django.contrib import admin

from ForumApp.accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass
