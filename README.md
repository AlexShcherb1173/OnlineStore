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
└── templates
    ├── add_product.html  ← страница добавления товара
    └── home.html         ← пагинация и карточки товаров

### ✅ Результат
Возможность&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Описание  
✏️ Добавление товара	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Пользователь может добавить новый товар через веб-форму  
🧭 Навигация	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Постраничный просмотр каталога  
💾 ORM-сохранение&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;	Данные записываются напрямую в PostgreSQL  
🧱 Bootstrap	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Все формы и карточки оформлены в едином стиле  
📸 Изображения	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Поддерживается загрузка и отображение картинок  

## 📅 Обновление проекта — 2025-10-11
### 🔥 Новые возможности и изменения в структуре проекта
#### 🧩 1. Приложение catalog — переход на CBV (Class-Based Views)
* Переведены все контроллеры (ранее FBV) на CBV (Class-Based Views):
* HomeView (наследуется от ListView) — отображение списка товаров с пагинацией (по 8 товаров на страницу).
* ProductDetailView (от DetailView) — отображение карточки конкретного товара.
* AddProductView (от CreateView) — форма добавления нового товара через ProductForm.
* ContactsView (от TemplateView с поддержкой формы) — страница с контактной формой и обратной связью.
* Для всех классов добавлены развёрнутые докстринги (описание логики, аргументов, возвращаемых данных и поведения).
* Обновлён файл urls.py под CBV-архитектуру:
from django.urls import path
from .views import HomeView, ProductDetailView, AddProductView, ContactsView
app_name = "catalog"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("add-product/", AddProductView.as_view(), name="add_product"),
]
#### 📰 2. Создано новое приложение blog
* Добавлено в INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    "blog",
]
* Создана модель Post со следующими полями:
title — заголовок поста;
content — основное содержимое;
preview — изображение-превью (загружается в /media/blog_previews/);
created_at — дата и время создания (автоматически);
is_published — булевый флаг публикации;
views_count — количество просмотров.
* Реализован полный CRUD (Create / Read / Update / Delete) на основе Class-Based Views:
PostListView — вывод всех опубликованных постов;
PostDetailView — просмотр отдельного поста, с автоматическим увеличением счётчика просмотров;
PostCreateView — создание нового поста с валидацией и автоперенаправлением на детальную страницу;
PostUpdateView — редактирование существующего поста;
PostDeleteView — удаление поста с подтверждением.
* Настроен файл blog/urls.py с namespace blog::
app_name = "blog"
urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("create/", PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
]
#### 📩 3. Новая бизнес-логика: автоматическое уведомление о достижении 100 просмотров
* В модели Post реализован механизм отправки письма владельцу сайта, если публикация достигает 100 просмотров.
* Письмо содержит поздравление и данные о посте.
* Реализовано в методе save() модели:
* if old_post and old_post.views_count < 100 <= self.views_count:
    send_mail(
        subject="🎉 Поздравляем с достижением 100 просмотров!",
        message=f"Ваш пост «{self.title}» набрал 100 просмотров!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["alex@example.com"],
    )
#### Требуется настроить SMTP в settings.py, например:
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_app_password"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

### 🧠 4. Технические улучшения
* Добавлены подробные докстринги для всех контроллеров, моделей и ключевых методов (с описанием логики, параметров и возвращаемых значений).
* В PostCreateView добавлен метод get_success_url(), который перенаправляет пользователя на страницу только что созданного поста, а не на список:
def get_success_url(self):
    return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})

### 🧱 5. Структура проекта после обновления
OnlineStore/  
│  
├── catalog/  
│   ├── views.py  ← все контроллеры на CBV  
│   ├── urls.py   ← обновлён под CBV  
│   ├── forms.py  
│   ├── models.py  
│   └── templates  
│  
├── blog/  
│   ├── models.py      ← модель Post + логика уведомлений  
│   ├── views.py       ← CRUD на CBV  
│   ├── urls.py        ← namespace "blog"  
│   └── templates  
│  
│  
└── config/  
    ├── settings.py  
    └── urls.py  

### 📬 Настройка SMTP и уведомлений

Для отправки почты проект использует встроенный механизм Django (django.core.mail.send_mail)
и настройки, вынесенные в файл .env.

### 🔧 Пример .env
#### PostgreSQL
DATABASE_NAME=onlinestore_db
DATABASE_USER=alex_postgres
DATABASE_PASSWORD=12345
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432

#### SMTP для Mail.ru
EMAIL_HOST=smtp.mail.ru
EMAIL_PORT=587
EMAIL_HOST_USER=myemail@mail.ru
EMAIL_HOST_PASSWORD=superpassword
EMAIL_USE_TLS=True

#### E-mail администратора (для уведомлений о 100 просмотрах поста)
ADMIN_EMAIL=alex@example.com

### ⚙️ Настройки в settings.py
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

#### Основной email администратора для уведомлений
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")

### 📨 Отправка уведомлений о достижении 100 просмотров

В модели Post реализована логика автоматической отправки поздравления,
когда количество просмотров (views_count) достигает 100.
Сообщение уходит на почту, указанную в .env:

recipient_list=[settings.ADMIN_EMAIL]

### 📎 Пример письма:
Тема: 🎉 Поздравляем с достижением 100 просмотров!
Текст:
Ваш пост «Как я подключил Django к PostgreSQL» набрал 100 просмотров!
Поздравляем! Это отличное достижение 🎯
Продолжайте писать — аудитория растёт!