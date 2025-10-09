from django.db import models


class Category(models.Model):
    """Модель категории товара."""
    name = models.CharField(max_length=100, unique=True, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара."""
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Изображение")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Contact(models.Model):
    """
    Модель для хранения контактной информации компании.
    """
    name = models.CharField(max_length=200, verbose_name="Название компании")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    about = models.TextField(blank=True, verbose_name="Описание / информация о компании")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.name
