from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from catalog.models import Product

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, **kwargs):
    """Сброс кеша списка продуктов при изменении или удалении."""
    if settings.CACHE_ENABLED:
        cache.delete("catalog:products:list")