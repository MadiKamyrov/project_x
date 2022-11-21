from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BuiltinUserAdmin
from django.utils.translation import gettext_lazy as _
from knox.models import AuthToken

from user.models import User


class UserAdmin(BuiltinUserAdmin):
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "roles",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "first_name", "last_name")
    ordering = ('-id',)
    save_on_top = True


class CustomAuthTokenAdmin(admin.ModelAdmin):
    list_display = ('digest', 'user', 'created',)
    raw_id_fields = ('user',)
    search_fields = ('user__email',)
    readonly_fields = ('created',)
    date_hierarchy = 'created'


admin.site.unregister(AuthToken)
admin.site.register(AuthToken, CustomAuthTokenAdmin)
admin.site.register(User, UserAdmin)