from django.core.cache import cache
from django.conf import settings
from catalog.models import Product


def get_products_by_category(category_id):
    """Возвращает список всех продуктов в указанной категории.
    Если включён кэш, то кэширует результат на CACHE_TTL секунд."""
    cache_key = f"category_products:{category_id}"
    cache_ttl = getattr(settings, "CACHE_TTL", 300)

    if getattr(settings, "CACHE_ENABLED", False):
        products = cache.get(cache_key)
        if products is not None:
            return products

    products = list(
        Product.objects.filter(category_id=category_id, is_published=True)
        .select_related("category")
        .order_by("-created_at")
    )

    if getattr(settings, "CACHE_ENABLED", False):
        cache.set(cache_key, products, cache_ttl)

    return products