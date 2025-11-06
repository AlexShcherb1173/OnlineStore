from django.conf import settings
from django.core.cache import cache

HOME_CACHE_KEY_PUBLIC = "home:products:public"
HOME_CACHE_KEY_STAFF = "home:products:staff"


def invalidate_home_products():
    """Чистит оба ключа кэша списка товаров на главной."""
    if getattr(settings, "CACHE_ENABLED", False):
        cache.delete_many([HOME_CACHE_KEY_PUBLIC, HOME_CACHE_KEY_STAFF])


def home_key(is_staff: bool) -> str:
    return HOME_CACHE_KEY_STAFF if is_staff else HOME_CACHE_KEY_PUBLIC
