from django.core.exceptions import ValidationError
from django.db import models

# 🚫 Запрещённые слова (проверяются без учёта регистра)
BANNED_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


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
    """Модель товара.
    Модельная валидация (clean) запрещает:
      - отрицательные цены,
      - использование BANNED_WORDS в полях name и description (без учёта регистра).
    save() вызывает full_clean(), чтобы валидация срабатывала везде:
    в админке, в пользовательских формах, через ORM и shell."""

    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    # ---------- ВАЛИДАЦИЯ МОДЕЛИ ----------
    def clean(self):
        """Глобальная валидация модели (исполняется из full_clean())."""
        errors = {}

        # 1) Цена не может быть отрицательной
        if self.price is not None and self.price < 0:
            errors["price"] = "Цена не может быть отрицательной."

        # 2) Запрещённые слова в name/description
        def hits(text: str) -> list[str]:
            if not text:
                return []
            low = text.lower()
            return [w for w in BANNED_WORDS if w in low]

        bad_in_name = hits(self.name or "")
        if bad_in_name:
            errors["name"] = (
                f"В названии обнаружены запрещённые слова: {', '.join(bad_in_name)}."
            )

        bad_in_desc = hits(self.description or "")
        if bad_in_desc:
            errors["description"] = (
                f"В описании обнаружены запрещённые слова: {', '.join(bad_in_desc)}."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Гарантируем запуск валидации модели перед сохранением."""
        self.full_clean()  # запускает clean() и field-level проверки
        super().save(*args, **kwargs)


class Contact(models.Model):
    """Модель для хранения контактной информации компании."""

    name = models.CharField(max_length=200, verbose_name="Название компании")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    about = models.TextField(
        blank=True, verbose_name="Описание / информация о компании"
    )

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.name
