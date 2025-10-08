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