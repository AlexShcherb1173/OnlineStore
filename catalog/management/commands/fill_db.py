import random
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from faker import Faker


class Command(BaseCommand):
    """
    Универсальная команда для заполнения базы данных:
    - очищает старые данные;
    - добавляет тестовые категории и товары;
    - умеет работать с фикстурами (--from-fixtures);
    - умеет генерировать случайные товары (--count N);
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

    def handle(self, *args, **options):
        fake = Faker("ru_RU")

        self.stdout.write("🧹 Очищаем базу данных...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # === 1. Если загружаем из фикстур ===
        if options["from_fixtures"]:
            self.stdout.write("📂 Загружаем данные из фикстур...")
            try:
                call_command("loaddata", "catalog/fixtures/categories.json")
                call_command("loaddata", "catalog/fixtures/products.json")
                self.stdout.write(self.style.SUCCESS("✅ Данные успешно загружены из фикстур!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Ошибка при загрузке фикстур: {e}"))
            return  # 🔹 выходим — больше ничего не делаем

        # === 2. Создаём категории (только если не from-fixtures) ===
        self.stdout.write("📦 Создаём категории...")
        categories = [
            Category.objects.create(name="Электроника", description="Гаджеты и техника"),
            Category.objects.create(name="Одежда", description="Мужская и женская одежда"),
            Category.objects.create(name="Книги", description="Печатные и электронные издания"),
            Category.objects.create(name="Бытовая техника", description="Техника для дома"),
        ]

        # === 3. Если указан --count — генерируем случайные товары ===
        if options["count"] > 0:
            count = options["count"]
            self.stdout.write(f"🎲 Генерируем {count} случайных продуктов...")

            for _ in range(count):
                category = random.choice(categories)
                name = fake.sentence(nb_words=3).replace(".", "")
                description = fake.text(max_nb_chars=120)
                price = round(random.uniform(100, 50000), 2)

                Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Сгенерировано {count} продуктов!"))
            return

        # === 4. Если нет count — добавляем фиксированные тестовые данные ===
        self.stdout.write("🛠 Создаём стандартные тестовые товары...")

        electronics, clothes, books, appliances = categories

        Product.objects.create(
            name="Смартфон Samsung S24",
            description="Флагман 2025 года, 256 ГБ",
            price=89990,
            category=electronics,
        )
        Product.objects.create(
            name="Ноутбук Lenovo ThinkPad X1",
            description="Core i7, 32 ГБ RAM, SSD 1 ТБ",
            price=189990,
            category=electronics,
        )
        Product.objects.create(
            name="Футболка белая",
            description="100% хлопок, размер M",
            price=1490,
            category=clothes,
        )
        Product.objects.create(
            name="Книга 'Django для начинающих'",
            description="Пошаговое руководство по Django 5.0",
            price=990,
            category=books,
        )
        Product.objects.create(
            name="Пылесос Dyson V15",
            description="Беспроводной пылесос премиум-класса",
            price=49990,
            category=appliances,
        )

        self.stdout.write(self.style.SUCCESS("✅ База успешно заполнена тестовыми данными!"))
        self.stdout.write(self.style.SUCCESS("🎉 Команда fill_db завершена успешно!"))