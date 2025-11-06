from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from catalog.models import Product
from catalog.cache_utils import invalidate_home_products


@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, **kwargs):
    """Сброс кеша списка продуктов при изменении или удалении."""
    if settings.CACHE_ENABLED:
        cache.delete("catalog:products:list")


@receiver(post_save, sender=Product)
def product_saved_invalidate_cache(sender, instance: Product, **kwargs):
    # Любое создание/редактирование товара
    invalidate_home_products()


@receiver(post_delete, sender=Product)
def product_deleted_invalidate_cache(sender, instance: Product, **kwargs):
    # Удаление товара
    invalidate_home_products()
