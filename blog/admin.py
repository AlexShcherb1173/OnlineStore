from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки отображения модели Post в админке Django."""

    # 📋 Какие поля показывать в списке
    list_display = (
        "id",
        "title",
        "is_published",
        "views_count",
        "created_at",
        "preview_image",
    )

    # 🔍 По каким полям искать
    search_fields = ("title", "content")

    # 🧩 Фильтры справа
    list_filter = ("is_published", "created_at")

    # 🕒 Сортировка по умолчанию
    ordering = ("-created_at",)

    # 📅 Только для чтения поля (не редактируются вручную)
    readonly_fields = ("views_count", "created_at")

    # 🧾 Поля, доступные в форме
    fields = (
        "title",
        "content",
        "preview",
        "is_published",
        "views_count",
        "created_at",
    )

    def preview_image(self, obj):
        """Отображает миниатюру превью прямо в списке."""
        if obj.preview:
            return format_html('<img src="{}" width="80" style="border-radius:8px;">', obj.preview.url)
        return "—"

    preview_image.short_description = "Превью"
    preview_image.allow_tags = True
