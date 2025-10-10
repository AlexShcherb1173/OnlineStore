import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Заполняет базу реальными товарами с картинками из интернета"

    def download_image(self, url, filename):
        """
        Скачивает изображение по url и возвращает Django ContentFile,
        или None, если не удалось скачать.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return ContentFile(response.content, name=filename)
        except Exception as e:
            self.stderr.write(f"Ошибка скачивания изображения {url}: {e}")
            return None

    def handle(self, *args, **options):
        # Очистка старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Категории
        names = {
            "Электроника": "Гаджеты, техника и электроника",
            "Одежда": "Мужская и женская одежда",
            "Книги": "Книги, литература",
            "Бытовая техника": "Приборы для дома",
        }
        cats = {}
        for name, desc in names.items():
            c = Category.objects.create(name=name, description=desc)
            cats[name] = c
            self.stdout.write(self.style.SUCCESS(f"Категория создана: {name}"))

        # Данные товаров: примерная заготовка с URL картинок
        # Лучше заменить эти URL на рабочие ссылки с картинками, которые ты хотите использовать.
        products_list = []

        # Электроника (8)
        products_list += [
            {
                "name": "Apple iPhone 14 Pro",
                "description": "Смартфон Apple с Pro-камерой и дисплеем ProMotion.",
                "price": 999.99,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9",
            },
            {
                "name": "Samsung Galaxy Z Fold 5",
                "description": "Складной смартфон Samsung с гибким экраном.",
                "price": 1899.99,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1580894908361-6eca2f151369",
            },
            {
                "name": "Sony WH-1000XM5",
                "description": "Премиальные накладные наушники с шумоподавлением.",
                "price": 349.0,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1593642634315-48f5414c3ad9",
            },
            {
                "name": "Apple MacBook Air M2",
                "description": "Лёгкий ноутбук Apple с процессором M2.",
                "price": 1299.0,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8",
            },
            {
                "name": "GoPro Hero 11",
                "description": "Экшн-камера высокого качества.",
                "price": 499.0,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1593642532973-d31b6557fa68",
            },
            {
                "name": "Apple iPad Pro",
                "description": "Планшет Apple с M-серией чипов.",
                "price": 1099.0,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1554755228-7a0ae820dcb2",
            },
            {
                "name": "Fitbit Charge 6",
                "description": "Фитнес-браслет с множеством датчиков.",
                "price": 179.99,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1572172355158-9a854a6d3f7a",
            },
            {
                "name": "DJI Mini 4 Pro",
                "description": "Компактный дрон с 4K-видео.",
                "price": 749.0,
                "category": cats["Электроника"],
                "image_url": "https://images.unsplash.com/photo-1593642632871-8b12e02d091c",
            },
        ]

        # Одежда (8)
        products_list += [
            {
                "name": "Nike Air Max 270",
                "description": "Спортивные кроссовки с воздушной подушкой.",
                "price": 150.0,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
            },
            {
                "name": "Adidas Ultraboost 23",
                "description": "Кроссовки с максимальной амортизацией Boost.",
                "price": 180.0,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1519183071298-a2962be54afa",
            },
            {
                "name": "Levi's 501 Original",
                "description": "Классические джинсы Levi’s.",
                "price": 69.99,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f",
            },
            {
                "name": "The North Face пуховик",
                "description": "Тёплая зимняя куртка с пуховой набивкой.",
                "price": 250.0,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1600181952931-7e8cbea7d318",
            },
            {
                "name": "H&M Basic T-Shirt",
                "description": "Стандартная футболка из хлопка.",
                "price": 19.99,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1602810312808-993fb76ecdc0",
            },
            {
                "name": "Gucci Leather Belt",
                "description": "Роскошный ремень из кожи.",
                "price": 399.99,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1585079540576-3b22956f40f9",
            },
            {
                "name": "Zara Oxford Shirt",
                "description": "Рубашка Oxford класса премиум.",
                "price": 39.50,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1556909200-50d42cf063a1",
            },
            {
                "name": "Patagonia T-shirt",
                "description": "Экологичная футболка из переработанных материалов.",
                "price": 59.0,
                "category": cats["Одежда"],
                "image_url": "https://images.unsplash.com/photo-1536305030467-df84cd545e5f",
            },
        ]

        # Книги (8)
        products_list += [
            {
                "name": "1984 — George Orwell",
                "description": "Антиутопический роман о тоталитарном обществе.",
                "price": 12.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1529655683826-aba9b3e77383",
            },
            {
                "name": "Sapiens — Yuval Noah Harari",
                "description": "История человечества в одном томе.",
                "price": 19.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b",
            },
            {
                "name": "Clean Code — Robert C. Martin",
                "description": "Руководство по написанию чистого кода.",
                "price": 34.50,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1496104679561-38ab7310f535",
            },
            {
                "name": "The Pragmatic Programmer",
                "description": "Современные рекомендации программистам.",
                "price": 27.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794",
            },
            {
                "name": "Harry Potter and the Sorcerer’s Stone",
                "description": "Фантастика, начало серии про Гарри Поттера.",
                "price": 15.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1528207776546-365bb710ee93",
            },
            {
                "name": "Clean Architecture — Robert C. Martin",
                "description": "Принципы чистой архитектуры программного обеспечения.",
                "price": 31.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f",
            },
            {
                "name": "Deep Work — Cal Newport",
                "description": "О влиянии сосредоточенного труда.",
                "price": 24.0,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1496104679561-38ab7310f535",
            },
            {
                "name": "The Hobbit — J.R.R. Tolkien",
                "description": "Фэнтези-приключение в Средиземье.",
                "price": 15.99,
                "category": cats["Книги"],
                "image_url": "https://images.unsplash.com/photo-1551024601-bec78aea704b",
            },
        ]

        # Бытовая техника (8)
        products_list += [
            {
                "name": "Dyson V15 Detect",
                "description": "Вертикальный пылесос с сенсорной технологией.",
                "price": 599.0,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1591012961303-7e3f04f517d4",
            },
            {
                "name": "Samsung Bespoke Refrigerator",
                "description": "Холодильник с модульным дизайном.",
                "price": 2499.0,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2",
            },
            {
                "name": "LG OLED C3 TV",
                "description": "OLED телевизор 55 дюймов.",
                "price": 1499.99,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1611976249270-871d49b66270",
            },
            {
                "name": "Breville Espresso Machine",
                "description": "Эспрессо-машина премиум-класса.",
                "price": 899.99,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1600181952931-7e8cbea7d318",
            },
            {
                "name": "Instant Pot Duo 7-in-1",
                "description": "Мультиварка / скороварка 7 в 1.",
                "price": 119.99,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e677",
            },
            {
                "name": "Dyson Purifier Cool",
                "description": "Очиститель воздуха + вентилятор.",
                "price": 499.99,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1600181952931-7e8cbea7d318",
            },
            {
                "name": "iRobot Roomba j7+",
                "description": "Робот-пылесос с автоматическим сливом.",
                "price": 799.0,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1600181952931-7e8cbea7d318",
            },
            {
                "name": "Philips Air Fryer",
                "description": "Аэрогриль для здоровой жарки.",
                "price": 199.99,
                "category": cats["Бытовая техника"],
                "image_url": "https://images.unsplash.com/photo-1600181952931-7e8cbea7d318",
            },
        ]

        # Теперь создаём объекты Product
        for idx, pdata in enumerate(products_list, start=1):
            prod = Product(
                name=pdata["name"],
                description=pdata["description"],
                price=pdata["price"],
                category=pdata["category"],
            )

            # Скачиваем картинку и сохраняем, если получилось
            img_content = self.download_image(pdata["image_url"], f"prod_{idx}.jpg")
            if img_content:
                prod.image.save(f"prod_{idx}.jpg", img_content, save=False)

            prod.save()
            self.stdout.write(self.style.SUCCESS(f"Создан товар: {prod.name}"))

        self.stdout.write(self.style.SUCCESS("✅ Все товары созданы успешно!"))
