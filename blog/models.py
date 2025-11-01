from django.db import models
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    """Блог-пост:
    - title, content, preview
    - author (для прав и подписи)
    - is_published (отображение в списке)
    - views_count (счётчик)
    При первом достижении 100 просмотров отправляет письмо администратору."""

    title = models.CharField(_("Заголовок"), max_length=200)
    content = models.TextField(_("Содержимое"))

    # 👇 добавили автора (совместимо с AUTH_USER_MODEL)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("Автор"),
        related_name="posts",
        null=True,  # ← временно, чтобы не упасть на существующих данных
        blank=True,
    )

    preview = models.ImageField(
        _("Превью (изображение)"),
        upload_to="blog_previews/",
        blank=True,
        null=True,
        help_text=_("Показывается в списке постов."),
    )

    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    # 👇 по умолчанию публикуем, чтобы список не был пуст
    is_published = models.BooleanField(_("Опубликован"), default=True)

    views_count = models.PositiveIntegerField(_("Количество просмотров"), default=0)

    class Meta:
        verbose_name = _("Блоговая запись")
        verbose_name_plural = _("Блоговые записи")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["is_published"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает ссылку на просмотр этой статьи."""
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """Отправляем письмо один раз при первом переходе порога 100 просмотров."""
        send_congrats = False
        if self.pk:
            old = Post.objects.only("views_count").filter(pk=self.pk).first()
            if old and old.views_count < 100 <= self.views_count:
                send_congrats = True

        super().save(*args, **kwargs)

        if send_congrats:
            try:
                send_mail(
                    subject="🎉 Пост набрал 100+ просмотров",
                    message=(
                        f"Пост «{self.title}» достиг {self.views_count} просмотров.\n"
                        "Так держать!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception:
                # умышленно не роняем сохранение поста
                pass


# без доп задания
# class Post(models.Model):
#     """Модель блоговой записи."""
#
#     title = models.CharField(max_length=200, verbose_name="Заголовок")
#     content = models.TextField(verbose_name="Содержимое")
#     preview = models.ImageField(upload_to="blog_previews/", blank=True, null=True, verbose_name="Превью")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
#     is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
#     views_count = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
#
#     class Meta:
#         verbose_name = "Пост"
#         verbose_name_plural = "Посты"
#         ordering = ["-created_at"]
#
#     def __str__(self):
#         return self.title
