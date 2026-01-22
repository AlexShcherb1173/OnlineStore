from .settings import *  # noqa

# --- базовые тестовые настройки ---
DEBUG = False
SECRET_KEY = "test-secret-key"
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]

# --- база: SQLite in-memory (чтобы не зависеть от Postgres локально) ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# --- кеш: локальный (никакого Redis в тестах) ---
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
}
CACHE_ENABLED = False
CACHE_TTL = 60

# --- ускоряем тесты ---
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"