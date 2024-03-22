from django.contrib import admin

from accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_login",
        "name",
        "email",
        "is_active",
        "is_admin",
        "date_joined",
        "last_update",
    )
    list_filter = (
        "last_login",
        "is_active",
        "is_admin",
        "date_joined",
        "last_update",
    )
    search_fields = ("USERNAME_FIELD",)
