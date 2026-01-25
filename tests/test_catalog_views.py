import pytest
from django.core.cache import cache
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_home_page_ok(client, disable_cache):
    r = client.get("/")
    assert r.status_code == 200


def test_contacts_get_ok(client):
    r = client.get("/contacts/")
    assert r.status_code == 200
    # форма должна быть в контексте
    assert "form" in r.context


def test_contacts_post_valid_shows_success_message(client):
    r = client.post("/contacts/", data={"name": "Alex", "phone": "79001234567", "message": "Hi"})
    assert r.status_code == 200
    assert r.context["success_message"] is not None
    assert "Спасибо" in r.context["success_message"]


def test_contacts_post_invalid_no_success_message(client):
    r = client.post("/contacts/", data={"name": "Alex", "phone": "BAD", "message": "Hi"})
    assert r.status_code == 200
    assert r.context["success_message"] is None
    assert r.context["form"].errors


def test_product_detail_public_sees_only_published(client, django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    published = baker.make("catalog.Product", category=cat, owner=user, price=10, is_published=True)
    hidden = baker.make("catalog.Product", category=cat, owner=user, price=10, is_published=False)

    r1 = client.get(f"/product/{published.pk}/")
    assert r1.status_code == 200

    r2 = client.get(f"/product/{hidden.pk}/")
    assert r2.status_code == 404


def test_product_detail_staff_sees_unpublished(client, django_user_model):
    staff = baker.make(django_user_model, is_staff=True)
    client.force_login(staff)

    cat = baker.make("catalog.Category")
    hidden = baker.make("catalog.Product", category=cat, owner=staff, price=10, is_published=False)

    r = client.get(f"/product/{hidden.pk}/")
    assert r.status_code == 200


def test_home_queryset_filters_for_public_and_staff(client, django_user_model, disable_cache):
    owner = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    baker.make("catalog.Product", category=cat, owner=owner, price=1, is_published=True, _quantity=3)
    baker.make("catalog.Product", category=cat, owner=owner, price=1, is_published=False, _quantity=2)

    # public: только опубликованные
    r = client.get("/")
    assert r.status_code == 200
    products = list(r.context["products"])
    assert all(p.is_published for p in products)

    # staff: видит все
    staff = baker.make(django_user_model, is_staff=True)
    client.force_login(staff)
    r2 = client.get("/")
    products2 = list(r2.context["products"])
    assert len(products2) >= len(products)


def test_home_cache_branch_uses_cache_for_public(client, enable_cache, django_user_model):
    cache.clear()

    owner = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    baker.make("catalog.Product", category=cat, owner=owner, price=1, is_published=True, _quantity=2)

    # 1-й вызов прогреет кэш
    r1 = client.get("/")
    assert r1.status_code == 200

    # 2-й вызов должен взять из кэша (проверяем косвенно: кэш-ключ существует)
    cache_key = "home:products:public"
    assert cache.get(cache_key) is not None
    r2 = client.get("/")
    assert r2.status_code == 200