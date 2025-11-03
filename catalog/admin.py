from django.contrib import admin
from .models import Product, Category, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в админке."""

    list_display = ("id", "name")  # Показываем id и имя
    search_fields = ("name",)  # Поиск по названию


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение товаров в админке."""

    list_display = (
        "id",
        "name",
        "price",
        "category",
        "is_published",
    )  # Выводим нужные поля
    list_editable = ("is_published",)
    list_filter = (
        "category",
        "is_published",
    )  # Фильтрация по категории
    search_fields = ("name", "description")

    actions = ("make_published", "make_unpublished")

    @admin.action(description="Опубликовать выбранные")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации выбранные")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "address")
