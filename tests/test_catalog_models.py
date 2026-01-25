import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker

pytestmark = pytest.mark.django_db


def test_category_str():
    c = baker.make("catalog.Category", name="Phones")
    assert str(c) == "Phones"


def test_contact_str():
    contact = baker.make("catalog.Contact", name="My Company")
    assert str(contact) == "My Company"


def test_product_str_includes_category_name(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category", name="C1")
    p = baker.make("catalog.Product", name="P1", category=cat, owner=user, price=10, is_published=True)
    assert str(p) == "P1 (C1)"


def test_product_negative_price_raises_validation_error(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")
    p = baker.prepare("catalog.Product", name="Ok", category=cat, owner=user, price=-1)

    with pytest.raises(ValidationError) as exc:
        p.save()  # save() вызывает full_clean()

    assert "price" in exc.value.message_dict


def test_product_banned_word_in_name_raises(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")
    p = baker.prepare("catalog.Product", name="Супер казино", description="ok", category=cat, owner=user, price=1)

    with pytest.raises(ValidationError) as exc:
        p.save()

    assert "name" in exc.value.message_dict


def test_product_banned_word_in_description_raises(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")
    p = baker.prepare("catalog.Product", name="Ok", description="тут крипта", category=cat, owner=user, price=1)

    with pytest.raises(ValidationError) as exc:
        p.save()

    assert "description" in exc.value.message_dict


def test_get_absolute_url(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")
    p = baker.make("catalog.Product", category=cat, owner=user, price=1)
    assert p.get_absolute_url().endswith(f"/product/{p.pk}/")