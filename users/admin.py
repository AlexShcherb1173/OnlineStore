from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Кастомная админка для модели User с логином по email."""

    # Поля, которые показываем в списке
    list_display = ("id", "email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Поля только для чтения (id/даты)
    readonly_fields = ("last_login", "date_joined")

    # Поля для поиска
    search_fields = ("email", "first_name", "last_name")
    ordering = ("id",)

    # Настройка форм редактирования
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Персональная информация"), {"fields": ("first_name", "last_name", "avatar", "phone", "country")}),
        (_("Права доступа"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )

    # Настройка формы создания
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
