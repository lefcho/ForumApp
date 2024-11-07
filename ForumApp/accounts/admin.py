from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from ForumApp.accounts.forms import CustomUserForm, CustomUserChangeForm
from ForumApp.accounts.models import Profile

UserModel = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fields = ('age', 'points', )


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    form = CustomUserChangeForm
    add_form = CustomUserForm

    list_display = ('username', 'email',)

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide', ),
                'fields': ('username', 'email', 'password', 'password2'),
            },
        ),
    )

    fieldsets = (
        ('Credentials', {'fields': ('email', 'password', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', )}),
    )