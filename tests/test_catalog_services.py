import pytest
from django.core.cache import cache
from model_bakery import baker

from catalog.services import get_products_by_category

pytestmark = pytest.mark.django_db


def test_get_products_by_category_returns_only_published(disable_cache, django_user_model):
    owner = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    pub = baker.make("catalog.Product", category=cat, owner=owner, price=10, is_published=True)
    baker.make("catalog.Product", category=cat, owner=owner, price=10, is_published=False)

    result = get_products_by_category(cat.id)

    assert pub in result
    assert all(p.is_published for p in result)


def test_get_products_by_category_cache_miss_sets_cache(enable_cache, django_user_model):
    cache.clear()

    owner = baker.make(django_user_model)
    cat = baker.make("catalog.Category")
    baker.make("catalog.Product", category=cat, owner=owner, price=10, is_published=True)

    key = f"category_products:{cat.id}"
    assert cache.get(key) is None

    result = get_products_by_category(cat.id)
    assert len(result) >= 1
    assert cache.get(key) is not None


def test_get_products_by_category_cache_hit_returns_cached(enable_cache, django_user_model):
    cache.clear()

    owner = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    # В БД ничего не создаём — проверяем, что отдаст именно кэш
    key = f"category_products:{cat.id}"
    sentinel = [{"fake": True}]
    cache.set(key, sentinel, 60)

    result = get_products_by_category(cat.id)
    assert result == sentinel