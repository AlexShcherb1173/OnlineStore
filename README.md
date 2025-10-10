# 🛒 OnlineStore

Учебный Django-проект интернет-магазина с каталогом товаров и формой обратной связи.  
В проекте используется **Django**, **Bootstrap 5.3.8** и **Font Awesome 7.1** (локальные версии через `/static`).  

---

## 📂 Структура проекта
OnlineStore/
│── catalog/ # Приложение "Каталог"  
│ │── migrations/ # Миграции БД  
│ │ └── init.py  
│ │── init.py  
│ │── admin.py # Админ-панель  
│ │── apps.py # Конфигурация приложения  
│ │── forms.py # Django-формы (например, обратная связь)  
│ │── models.py # Модели базы данных  
│ │── tests.py # Тесты  
│ │── urls.py # Маршруты приложения  
│ │── views.py # Контроллеры (home, contacts и др.)  
│  
│── config/ # Конфигурация проекта Django  
│ │── init.py  
│ │── asgi.py  
│ │── settings.py # Настройки Django  
│ │── urls.py # Маршруты проекта  
│ │── wsgi.py  
│
│── static/ # Локальные статические файлы  
│ │── bootstrap-5.3.8-dist/ # Bootstrap 5 (CSS + JS)  
│ │── fontawesome-free-7.1.0-web/ # Font Awesome (CSS + иконки)  
│  
│── templates  
│ │── catalog     
│     └──  contacts.html  
│     └──  home.html  
│── manage.py # Основная точка входа Django  
│── requirements.txt # Зависимости проекта (pip)  
│── poetry.toml # Конфигурация Poetry  
│── README.md # Документация проекта  
## ⚙️ Установка и запуск

### 1. Клонирование проекта
```bash
git clone https://github.com/AlexShcherb1173/OnlineStore.git
cd OnlineStore 
```
### 2. Создание виртуального окружения
#### Через venv
```bash
python -m venv .venv
.\.venv\Scripts\activate   # Windows PowerShell
# или
source .venv/bin/activate  # Linux/macOS
```
#### Через Poetry
```bash
poetry install
poetry shell
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Применение миграций
```bash
python manage.py migrate
```
### 5. Запуск сервера разработки
```bash
python manage.py runserver
```
Теперь проект будет доступен по адресу:  
👉 http://127.0.0.1:8000/

## 📌 Основные страницы

#### * Главная (/) — каталог товаров

#### * Контакты (/contacts/) — форма обратной связи с сообщением об успешной отправке

## 🎨 Используемые технологии

#### * Backend: Django 5+

#### * Frontend: Bootstrap 5.3.8, Font Awesome 7.1

#### * База данных: SQLite (по умолчанию)

#### * Управление зависимостями: Poetry / pip

## 🚀 TODO

 #### - Добавить авторизацию пользователей

 #### - Реализовать модели для каталога товаров

 #### - Подключить отправку писем из формы обратной связи

 #### - Подключить CI/CD и тестирование

## 📄 Лицензия

#### Этот проект распространяется под лицензией MIT.


# 📅 Обновление от 2025-10-05
## 🔗 Подключение PostgreSQL

##### Настроено подключение проекта Django к базе данных PostgreSQL.
#### Исправлены ошибки прав доступа и подключений (fe_sendauth, Permission denied, schema public).
#### Проверено создание базы и выполнение миграций.
#### В .env добавлены переменные окружения для базы данных:
POSTGRES_DB=mydatabase  
POSTGRES_USER=postgres  
POSTGRES_PASSWORD=your_password  
POSTGRES_HOST=localhost  
POSTGRES_PORT=5432  

### 🧩 Приложение catalog
#### 📦 Модели
#### Добавлены и зарегистрированы в админке модели:
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

class Product(models.Model):  
    name = models.CharField(max_length=255)  
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to="products/", blank=True, null=True)  
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

#### Дополнительно создана модель для страницы Контакты:

class Contact(models.Model):  
    name = models.CharField(max_length=200)  
    phone = models.CharField(max_length=50)  
    email = models.EmailField()  
    address = models.CharField(max_length=255)  
    about = models.TextField(blank=True)  

### 🧠 Отображение в админке
#### Category: вывод id, name
#### Product: вывод id, name, price, category, фильтрация по категории и поиск по названию и описанию
#### Contact: вывод id, name, phone, email, address
### ⚙️ Кастомная команда fill_db
#### Добавлена команда:
#### python manage.py fill_db
### Функциональность:
#### Полностью очищает базу перед заполнением.
#### Создаёт базовые категории и тестовые продукты.
#### Поддерживает три режима:
#### --from-fixtures — загрузка данных из JSON-фикстур;
#### --count N — генерация случайных товаров с помощью Faker;
#### --sample (по умолчанию) — добавление фиксированных тестовых данных.
### Пример использования:
#### python manage.py fill_db --count 20
### 🌐 Контроллеры и шаблоны
#### home_view
#### Отображает последние 5 добавленных продуктов:
#### latest_products = Product.objects.order_by('-created_at')[:5]
#### Результаты выводятся в консоль и на главной странице.
#### contacts_view
#### Загружает данные из модели Contact и отображает их в шаблоне.
#### Реализована форма обратной связи с CSRF-защитой и сообщением об успехе.
### 🎨 Обновлённые шаблоны
#### home.html
#### Динамически выводит 5 последних товаров в виде Bootstrap-карточек.
#### Отображает изображения (из поля image или случайные через picsum.photos).
#### Полностью адаптивная сетка и обновлённая структура футера.
#### contacts.html
#### Подключено динамическое отображение контактных данных из модели Contact.
#### Если данные не заполнены — показывается уведомление.
#### Оставлена форма обратной связи и общий стиль страницы.
### 🧭 Навигация
#### Добавлены маршруты:
#### path('', views.home_view, name='home')
#### path('contacts/', views.contacts_view, name='contacts')

#### Navbar синхронизирован с Django-URL-ами ({% url 'home' %}, {% url 'contacts' %}).

### 🧰 Инструменты

#### Установлена библиотека Faker для генерации случайных данных.
#### Созданы и протестированы фикстуры categories.json и products.json.
#### Проверено наполнение БД через Django shell и кастомные команды.

### ✅ Результат
#### Проект OnlineStore теперь:
#### Работает с PostgreSQL;
#### Имеет модели Product, Category и Contact;
#### Поддерживает заполнение тестовыми и случайными данными;
#### Отображает последние товары на главной;
#### Выводит контактные данные из БД на странице /contacts/;
#### Имеет обновлённые шаблоны с Bootstrap-дизайном и формой обратной связи.

## 🧱 Шаблонное наследование и переиспользование кода (обновление от 2025-10-08)

Чтобы сократить дублирование HTML-кода между страницами и упростить структуру проекта, в Django-приложении OnlineStore реализовано наследование шаблонов и инклюды общих компонентов.

### 📄 Базовый шаблон base.html

Создан шаблон, который содержит все общие элементы страниц:  
HTML-структура (doctype, head, body),  
подключение Bootstrap и Font Awesome,  
общий footer со ссылками и стилями,  
единая загрузка JS-скриптов.  
Каждая страница теперь наследует этот шаблон через директиву:  
{% extends "base.html" %}  

#### Блоки:

{% block title %}Заголовок страницы{% endblock %}  
{% block content %}Основной контент страницы{% endblock %}

### 🍔 Подшаблон меню includes/navbar.html

Вынесен навбар в отдельный подшаблон, подключаемый во все страницы:  
{% include "includes/navbar.html" %}  

#### Функциональность:

Навигация по сайту: Каталог, Контакты.  
Автоматическая подсветка активной страницы:  
{% if request.resolver_match.url_name == 'home' %}active{% endif %}

### 🏠 Главная страница (home.html)

Теперь наследует base.html и отображает список товаров в виде Bootstrap-карточек:  
ORM-запрос: Product.objects.all().order_by('-created_at')  
Данные: изображение, название, категория, цена, описание (сокращено до 100 символов)
через фильтр:  
{{ product.description|truncatechars:100 }}  
Кнопка перехода:  
<a href="{% url 'product_detail' product.pk %}">Подробнее</a>

### 📦 Страница одного товара (product_detail.html)

Получение объекта из БД по pk:  
product = get_object_or_404(Product, pk=pk)  
Отображение полной информации, включая фото, цену и дату создания.  
Кнопка «Вернуться к каталогу» возвращает на главную страницу.

### 📞 Страница контактов (contacts.html)

Использует base.html и includes/navbar.html.  
Загружает данные из модели Contact.  
Содержит таблицу с контактной информацией и форму обратной связи.

### ✅ Результат

После внедрения шаблонного наследования и инклюдов:  
Код шаблонов стал чище и короче (каждая страница теперь фокусируется только на своём контенте);  
Меню и подвал поддерживаются централизованно;  
Изменения в дизайне применяются ко всем страницам одновременно;  
Добавление новых страниц упрощено до пары строк.

### 🧭 Структура шаблонов проекта

В проекте реализована чистая иерархия шаблонов с наследованием и инклюдами:

templates/catalog  
│  
├── base.html                ← 🧱 Базовый шаблон  
│     ├── включает общие стили, footer, bootstrap  
│     └── {% include "includes/navbar.html" %}  
│  
├── includes/  
│     └── navbar.html        ← 🍔 Подшаблон главного меню (навигация)  
│  
├── home.html                ← 🏠 Главная страница  
│     └── {% extends "base.html" %}  
│  
├── contacts.html            ← 📞 Страница контактов  
│     └── {% extends "base.html" %}  
│  
└── product_detail.html      ← 🛒 Страница одного товара  
      └── {% extends "base.html" %}  


🔹 base.html — основной каркас сайта  
🔹 navbar.html — подключается к base и используется на всех страницах  
🔹 Остальные шаблоны переопределяют блоки:  

{% block title %}Заголовок{% endblock %}  
{% block content %}Контент страницы{% endblock %}  

## 🧾 Добавление товаров и постраничный вывод (обновление от 2025-10-09)
### 🛠️ Новая функциональность

В приложении Catalog реализована возможность:  
Добавлять новые товары через веб-форму  
Просматривать список товаров с постраничной навигацией (пагинацией)

### 🧩 1. Добавление новых товаров

URL: /add-product/  
Контроллер: add_product_view

🔹 Ключевые возможности:  
Используется ModelForm (ProductForm) для создания товаров.  
Поддерживается загрузка изображений через ImageField.  
После успешного сохранения выводится сообщение:  
✅ Товар "<название>" успешно добавлен!  
Ошибки валидации обрабатываются и отображаются пользователю.  
После добавления происходит перенаправление на главную страницу каталога.  

<u>📄 Пример формы:</u>   
class ProductForm(forms.ModelForm):  
    class Meta:  
        model = Product  
        fields = ["name", "description", "image", "category", "price"]  

<u>Шаблон: add_product.html</u>  
Форма оформлена в стиле Bootstrap и содержит кнопку «Вернуться к каталогу».  

### 📑 2. Пагинация списка товаров

<u>Контроллер: home_view</u>   
Теперь товары на главной странице отображаются постранично.  

paginator = Paginator(products, 8)  
page_number = request.GET.get("page")  
page_obj = paginator.get_page(page_number)  

<u>Шаблон: home.html</u>  
На странице показывается 8 товаров.  
Под карточками выводится навигация Bootstrap: 
[Предыдущая] 1 2 3 [Следующая]  
Все ссылки сохраняют URL-параметр ?page= для корректного перехода между страницами.  
Карточки товаров формируются циклом:  

{% for product in page_obj %}
    ...
{% endfor %}

### 📦 3. Обновлённая структура проекта
catalog/  
│  
├── forms.py              ← форма для создания товаров  
├── views.py              ← add_product_view + пагинация  
├── urls.py               ← маршрут /add-product/  
└── templates/catalog
    ├── add_product.html  ← страница добавления товара
    └── home.html         ← пагинация и карточки товаров

### ✅ Результат
Возможность&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Описание  
✏️ Добавление товара	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Пользователь может добавить новый товар через веб-форму  
🧭 Навигация	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Постраничный просмотр каталога  
💾 ORM-сохранение&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Данные записываются напрямую в PostgreSQL  
🧱 Bootstrap	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Все формы и карточки оформлены в едином стиле  
📸 Изображения	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поддерживается загрузка и отображение картинок  