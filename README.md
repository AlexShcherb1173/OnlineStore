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


