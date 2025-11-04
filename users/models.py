from __future__ import annotations

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер для пользователя с логином по email.
    Создаёт user/superuser, требуя валидный email и пароль."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # хешируем пароль
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя.
    - Логин по email (USERNAME_FIELD = 'email')
    - Поля: email (уникальный), avatar, phone, country
    - Поле username удалено (не используется)"""

    # Полностью убираем username из модели AbstractUser
    username = None

    email = models.EmailField(_("email address"), unique=True)

    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите изображение JPG/PNG",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон",
        validators=[
            RegexValidator(
                regex=r"^[\d\+\-\(\) ]{7,20}$",
                message="Телефон должен содержать 7–20 символов: цифры, + - ( ) и пробелы.",
            )
        ],
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Страна",
    )

    # Настройки аутентификации
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []  # при createsuperuser спросит только email и пароль

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.email
