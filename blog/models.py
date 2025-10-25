from django.db import models
from django.core.mail import send_mail
from django.conf import settings


class Post(models.Model):
    """Модель Blog Post — представляет публикацию (запись блога).

    Эта модель используется для хранения информации о блоговых записях, включая:
      - текстовую и графическую информацию (заголовок, содержимое, превью);
      - состояние публикации;
      - дату создания;
      - счётчик просмотров.

    Дополнительно реализована бизнес-логика:
      • при достижении 100 просмотров автоматически отправляется письмо владельцу сайта;
      • поле `views_count` увеличивается при каждом открытии детальной страницы (см. PostDetailView).

    Атрибуты:
        title (str): Заголовок публикации, отображается в списках и карточках постов.
        content (str): Основной текст записи (HTML или Markdown).
        preview (ImageField): Изображение-превью, отображается на карточках постов.
        created_at (datetime): Автоматически устанавливаемая дата и время создания поста.
        is_published (bool): Флаг, определяющий видимость поста на сайте.
        views_count (int): Количество просмотров поста. Увеличивается автоматически при каждом просмотре.

    Методы:
        __str__(): Возвращает строковое представление поста (его заголовок).
        save(): Переопределённый метод сохранения. Проверяет достижение 100 просмотров
                и отправляет уведомление по электронной почте."""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog_previews/",
        blank=True,
        null=True,
        verbose_name="Превью (изображение)",
        help_text="Изображение, отображаемое в списке постов или на главной странице блога.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликован")
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
        ordering = ["-created_at"]

    def __str__(self):
        """Возвращает строковое представление поста — его заголовок."""
        return self.title

    def save(self, *args, **kwargs):
        """Переопределённый метод сохранения объекта Post.
        Цель:
            Контролировать достижение определённого количества просмотров и
            автоматически уведомлять владельца проекта при достижении 100 просмотров.
        Логика работы:
            - При каждом вызове save() проверяется, существует ли уже объект в базе данных.
            - Если запись существует, выполняется сравнение старого и нового значения поля views_count.
            - Если счётчик просмотров вырос и впервые достиг значения >= 100,
              пользователю отправляется поздравительное письмо.
            - Для отправки используется функция send_mail() из Django.
        Аргументы:
            *args, **kwargs: передаются стандартные аргументы метода save() модели Django.
        Пример:
            post.views_count = 100
            post.save()
            → На почту alex@example.com будет отправлено письмо о достижении 100 просмотров.
        Примечание:
            Для работы почты необходимо корректно настроить SMTP в settings.py."""
        if self.pk:  # Проверяем, что объект уже существует (не создаётся впервые)
            old_post = Post.objects.filter(pk=self.pk).first()
            if old_post and old_post.views_count < 100 <= self.views_count:
                # Отправляем поздравительное письмо
                send_mail(
                    subject="🎉 Поздравляем с достижением 100 просмотров!",
                    message=(
                        f"Ваш пост «{self.title}» набрал 100 просмотров!\n\n"
                        "Поздравляем! Это отличное достижение 🎯\n"
                        "Продолжайте писать — аудитория растёт!"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],  # 👈 замени на свой email
                    fail_silently=False,
                )

        super().save(*args, **kwargs)


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
