# OnlineStore — Django e-commerce (PostgreSQL + Redis + Celery) + Docker Deploy

Django-проект интернет-магазина с каталогом товаров, блогом и пользователями.  
Продакшн-развёртывание через **Docker Compose + Nginx + Gunicorn**, фоновые задачи через **Celery**, кеширование через **Redis**.  
Проект оформлен как витрина: **реальный CI**, покрытие тестами, готовый production compose.

![CI](https://github.com/AlexShcherb1173/OnlineStore/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Django](https://img.shields.io/badge/Django-5.2%2B-green)
![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-blue)
![Redis](https://img.shields.io/badge/Cache-Redis-red)
![Celery](https://img.shields.io/badge/Tasks-Celery-brightgreen)
![Docker](https://img.shields.io/badge/Deploy-Docker-blue)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-black)
![Coverage](https://img.shields.io/badge/Coverage-75%25%2B-success)

---

## Содержание

- [Функционал](#функционал)
- [Технологии](#технологии)
- [Архитектура](#архитектура)
- [Быстрый старт (локально)](#быстрый-старт-локально)
- [Production Deploy (Docker Compose)](#production-deploy-docker-compose)
- [CI/CD (GitHub Actions)](#cicd-github-actions)
- [Переменные окружения](#переменные-окружения)
- [Полезные команды](#полезные-команды)

---

## Функционал

- Каталог товаров, карточка товара, изображения
- Пользователи и профили (аватар)
- Блог / контент (превью-изображение)
- Кеширование страниц/данных через Redis
- Фоновые задачи: Celery worker + Celery Beat
- Продакшн: Nginx (reverse proxy + static/media) → Gunicorn → Django

---

## Технологии

- **Python 3.12+**
- **Django 5.2+**
- **PostgreSQL 16**
- **Redis 7**
- **Celery 5**
- **Gunicorn**
- **Nginx**
- **Docker / Docker Compose**
- **pytest + pytest-django + coverage (порог 75%)**
- **GitHub Actions CI**

---

## Архитектура

```mermaid
flowchart LR
  U[User / Browser] -->|HTTP 80/443| N[Nginx]
  N -->|proxy_pass :8000| W[Gunicorn + Django (web)]
  N -->|/static| S[(static_volume)]
  N -->|/media| M[(media_volume)]

  W -->|SQL| P[(PostgreSQL)]
  W -->|cache| R[(Redis)]

  C[Celery worker] -->|broker| R
  B[Celery beat] -->|schedule| R
  C -->|DB ops| P

  subgraph Docker Compose Network
    N
    W
    P
    R
    C
    B
  end
 ```
Быстрый старт (локально)
1) Установка
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows PowerShell

pip install -r requirements.txt
2) Настроить переменные
Создай .env на основе .env.example (или вручную — см. раздел ниже).

3) Миграции и запуск
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Production Deploy (Docker Compose)
Структура на сервере
Рекомендуемая структура:

/opt/onlinestore  
├── docker-compose.prod.yml  
├── .env  
└── docker/  
    └── nginx/  
        └── default.conf  
Запуск на сервере (вариант B: pull && up)
cd /opt/onlinestore
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
docker compose -f docker-compose.prod.yml ps
Проверка, что всё работает
# Проверить, что порт 80 слушается
sudo ss -ltnp | grep ':80'

# Проверить ответ Nginx (локально на сервере)
curl -I http://127.0.0.1/

# Проверить главную страницу (получить HTML)
curl -s http://127.0.0.1/ | head   

# Проверить админку (должен быть 302 редирект на /admin/login/)  
curl -I http://127.0.0.1/admin/  
Если открываешь с компьютера:  

http://<PUBLIC_IP>/  
  
http://<PUBLIC_IP>/admin/    

CI/CD (GitHub Actions)  
Реальный CI badge  
Workflow:

.github/workflows/ci.yml  

Badge:

![CI](https://github.com/AlexShcherb1173/OnlineStore/actions/workflows/ci.yml/badge.svg)  
Flow: Tests → Build → Push → Deploy  
flowchart LR  
  A[Push / PR to main] --> CI[CI: pytest + coverage >= 75%]  
  CI -->|success| B[Build Docker images]  
  B --> P[Push to GHCR: ghcr.io/.../onlinestore/*:latest]  
  P --> D[Server deploy]  
  D -->|docker compose pull| R1[Pull images]  
  R1 -->|docker compose up -d| R2[Recreate containers]  
  R2 --> OK[✅ OnlineStore обновлён]  
Что делает CI (примерно)  
Устанавливает зависимости  

Запускает тесты pytest --cov --cov-fail-under=75

При успехе: собирает Docker-образы и пушит в GHCR:

ghcr.io/alexshcherb1173/onlinestore/web:latest

ghcr.io/alexshcherb1173/onlinestore/celery:latest

ghcr.io/alexshcherb1173/onlinestore/celery-beat:latest

Переменные окружения
Минимально важно (для production):

# Django
SECRET_KEY=...
DEBUG=0
ALLOWED_HOSTS=localhost,127.0.0.1,<PUBLIC_IP>

# Postgres
POSTGRES_DB=onlinestore
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis / cache
CACHE_ENABLED=1
CACHE_TTL=300
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB_CACHE=1
REDIS_CHECK_ENABLED=0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (пример)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  
EMAIL_HOST=smtp.gmail.com  
EMAIL_PORT=587  
EMAIL_USE_TLS=True  
EMAIL_USE_SSL=False  
EMAIL_HOST_USER=...  
EMAIL_HOST_PASSWORD=...  
DEFAULT_FROM_EMAIL=...  
SERVER_EMAIL=...  

TIME_ZONE=Europe/Amsterdam  
LANGUAGE_CODE=ru  
#### Полезные команды  
##### Логи и статусы    
docker compose -f docker-compose.prod.yml ps  
docker compose -f docker-compose.prod.yml logs -f web  
docker compose -f docker-compose.prod.yml logs -f nginx  
docker compose -f docker-compose.prod.yml logs -f celery  
docker compose -f docker-compose.prod.yml logs -f celery-beat  
##### Проверки внутри контейнера 
docker compose -f docker-compose.prod.yml exec web python -V  
docker compose -f docker-compose.prod.yml exec web python manage.py showmigrations
docker compose -f docker-compose.prod.yml exec web python manage.py check  
##### Обновление на сервере (после пуша в GHCR)  
cd /opt/onlinestore  
docker compose -f docker-compose.prod.yml pull  
docker compose -f docker-compose.prod.yml up -d   
GitHub Topics  

Статус  
✅ Проект развёрнут на сервере через Docker Compose  
✅ CI проходит тесты и поддерживает coverage threshold (75%+)  
✅ GHCR используется для push/pull образов и быстрого deploy  

::contentReference[oaicite:0]{index=0}