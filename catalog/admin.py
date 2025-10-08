from django.contrib import admin
from .models import Product, Category, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий в админке."""
    list_display = ("id", "name")  # Показываем id и имя
    search_fields = ("name",)       # Поиск по названию

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Отображение товаров в админке."""
    list_display = ("id", "name", "price", "category")  # Выводим нужные поля
    list_filter = ("category",)                         # Фильтрация по категории
    search_fields = ("name", "description")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "email", "address")
