from django.contrib import admin
from .models import Post


from django.contrib import admin
from django.utils.html import format_html
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки отображения модели Post в админке Django."""

    # Список
    list_display = (
        "id",
        "title",
        "is_published",
        "views_count",
        "created_at",
        "preview_image",   # миниатюра в списке
    )
    search_fields = ("title", "content")
    list_filter = ("is_published", "created_at")
    ordering = ("-created_at",)

    # Форма
    readonly_fields = ("views_count", "created_at", "preview_admin")  # предпросмотр в форме
    fields = (
        "title",
        "content",
        "preview",        # поле загрузки изображения
        "preview_admin",  # картинка-превью (только чтение)
        "is_published",
        "views_count",
        "created_at",
    )

    # --- РЕНДЕРЫ ИЗОБРАЖЕНИЙ ---

    def preview_image(self, obj):
        """Миниатюра в списке объектов."""
        if getattr(obj, "preview", None) and getattr(obj.preview, "url", None):
            return format_html(
                '<img src="{}" width="80" style="border-radius:8px; object-fit:cover;">',
                obj.preview.url,
            )
        return "—"
    preview_image.short_description = "Превью"

    def preview_admin(self, obj):
        """Крупный предпросмотр на странице изменения объекта."""
        if getattr(obj, "preview", None) and getattr(obj.preview, "url", None):
            return format_html(
                '<img src="{}" style="max-width: 320px; height:auto; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,.1);">',
                obj.preview.url,
            )
        return "Изображение не загружено"
    preview_admin.short_description = "Текущее изображение"
