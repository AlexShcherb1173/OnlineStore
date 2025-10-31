import io
import os
import uuid
import random
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from decimal import Decimal, ROUND_HALF_UP

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.core.management import call_command

from faker import Faker

from catalog.models import Category, Product


class Command(BaseCommand):
    """
    Универсальная команда для заполнения базы данных:
    - очищает старые данные;
    - добавляет тестовые категории и товары;
    - умеет работать с фикстурами (--from-fixtures);
    - умеет генерировать случайные товары (--count N);
    - автоматически подкладывает случайные изображения с picsum.photos;
    - безопасна — не создаёт дубликаты при загрузке фикстур.
    """

    help = "Очищает базу и заполняет её тестовыми данными, фикстурами или случайными товарами."

    def add_arguments(self, parser):
        parser.add_argument(
            "--from-fixtures",
            action="store_true",
            help="Загрузить данные из фикстур (catalog/fixtures/categories.json и products.json).",
        )
        parser.add_argument(
            "--sample",
            action="store_true",
            help="Создать стандартные тестовые данные вручную (по умолчанию).",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=0,
            help="Создать указанное количество случайных продуктов (использует Faker).",
        )

    # ---------- helpers ----------

    def _fetch_random_image(self, width: int = 600, height: int = 400) -> bytes | None:
        """
        Скачивает случайную картинку с picsum.photos и возвращает байты файла.
        Возвращает None, если загрузка не удалась.
        """
        seed = uuid.uuid4().hex  # уникальный сид, чтобы не кэшировалось одинаковое
        url = f"https://picsum.photos/seed/{seed}/{width}/{height}"
        try:
            with urlopen(url, timeout=10) as resp:  # urllib сам следует редиректам
                content = resp.read()
                # Простая страховка: размер > 1KB
                if len(content) > 1024:
                    return content
        except (URLError, HTTPError, TimeoutError) as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Не удалось загрузить изображение: {e}"))
        return None

    def _attach_random_image(self, product: Product, idx_hint: int | None = None) -> None:
        """
        Прикрепляет к продукту случайное изображение из picsum.
        Ошибки проглатываем, чтобы не ломать основной сценарий.
        """
        content = self._fetch_random_image()
        if not content:
            return
        # Имя файла в медиа-хранилище
        stem = f"prod_{product.pk or idx_hint or uuid.uuid4().hex}"
        filename = f"{stem}.jpg"  # picsum отдаёт jpeg по умолчанию
        try:
            product.image.save(filename, ContentFile(content), save=True)
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Не удалось сохранить файл изображения: {e}"))

    # ---------- main ----------

    def handle(self, *args, **options):
        fake = Faker("ru_RU")

        self.stdout.write("🧹 Очищаем базу данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # === 1) Фикстуры ===
        if options["from_fixtures"]:
            self.stdout.write("📂 Загружаем данные из фикстур...")
            try:
                call_command("loaddata", "catalog/fixtures/categories.json")
                call_command("loaddata", "catalog/fixtures/products.json")
                self.stdout.write(self.style.SUCCESS("✅ Данные успешно загружены из фикстур!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Ошибка при загрузке фикстур: {e}"))
            return

        # === 2) Категории ===
        self.stdout.write("📦 Создаём категории...")
        categories = [
            Category.objects.create(name="Электроника", description="Гаджеты и техника"),
            Category.objects.create(name="Одежда", description="Мужская и женская одежда"),
            Category.objects.create(name="Книги", description="Печатные и электронные издания"),
            Category.objects.create(name="Бытовая техника", description="Техника для дома"),
        ]

        # === 3) Случайные товары (--count) ===
        if options["count"] > 0:
            count = options["count"]
            self.stdout.write(f"🎲 Генерируем {count} случайных продуктов с изображениями...")
            products_batch = []
            for i in range(count):
                category = random.choice(categories)
                name = fake.sentence(nb_words=3).replace(".", "")
                description = fake.text(max_nb_chars=160)
                price_cents = random.randint(10_000, 5_000_000)  # от 100.00 до 50000.00
                price = (Decimal(price_cents) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                p = Product(
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                )
                p.save()
                # прикрепим картинки по одной, чтобы pk уже был
                self._attach_random_image(p, idx_hint=i + 1)
                products_batch.append(p)

            self.stdout.write(self.style.SUCCESS(f"✅ Сгенерировано {count} продуктов!"))
            return

        # === 4) Стандартный набор ===
        self.stdout.write("🛠 Создаём стандартные тестовые товары с изображениями...")
        electronics, clothes, books, appliances = categories

        items = [
            dict(name="Смартфон Samsung S24", description="Флагман 2025 года, 256 ГБ",
                 price=89990, category=electronics),
            dict(name="Ноутбук Lenovo ThinkPad X1", description="Core i7, 32 ГБ RAM, SSD 1 ТБ",
                 price=189990, category=electronics),
            dict(name="Футболка белая", description="100% хлопок, размер M",
                 price=1490, category=clothes),
            dict(name="Книга «Django для начинающих»", description="Пошаговое руководство по Django 5",
                 price=990, category=books),
            dict(name="Пылесос Dyson V15", description="Беспроводной пылесос премиум-класса",
                 price=49990, category=appliances),
        ]

        for i, data in enumerate(items, start=1):
            p = Product.objects.create(**data)
            self._attach_random_image(p, idx_hint=i)

        self.stdout.write(self.style.SUCCESS("✅ База успешно заполнена тестовыми данными!"))
        self.stdout.write(self.style.SUCCESS("🎉 Команда fill_db завершена успешно!"))