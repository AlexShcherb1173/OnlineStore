import pytest
import io
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.exceptions import ValidationError
from model_bakery import baker

from catalog.forms import ContactForm, ProductForm

pytestmark = pytest.mark.django_db


def test_contact_form_valid():
    form = ContactForm(data={"name": "Alex", "phone": "79001234567", "message": "Hi"})
    assert form.is_valid()


def test_contact_form_phone_invalid():
    form = ContactForm(data={"name": "Alex", "phone": "+7-900-123", "message": "Hi"})
    assert not form.is_valid()
    assert "phone" in form.errors


def test_contact_form_bootstrap_classes_added():
    form = ContactForm()
    assert "form-control" in form.fields["name"].widget.attrs.get("class", "")
    assert "form-control" in form.fields["phone"].widget.attrs.get("class", "")
    assert "form-control" in form.fields["message"].widget.attrs.get("class", "")


def test_product_form_banned_word_in_name(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    form = ProductForm(
        data={"name": "дешево купить", "description": "ok", "category": cat.pk, "price": "10.00"},
        user=user,
    )
    assert not form.is_valid()
    assert "name" in form.errors


def test_product_form_banned_word_in_description(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    form = ProductForm(
        data={"name": "ok", "description": "криптовалюта тут", "category": cat.pk, "price": "10.00"},
        user=user,
    )
    assert not form.is_valid()
    assert "description" in form.errors


def test_product_form_negative_price(django_user_model):
    user = baker.make(django_user_model)
    cat = baker.make("catalog.Category")

    form = ProductForm(
        data={"name": "ok", "description": "ok", "category": cat.pk, "price": "-1.00"},
        user=user,
    )
    assert not form.is_valid()
    assert "price" in form.errors


def test_product_form_adds_is_published_field_only_for_privileged_user(django_user_model):
    user = baker.make(django_user_model, is_staff=False)
    form = ProductForm(user=user)
    assert "is_published" not in form.fields

    staff = baker.make(django_user_model, is_staff=True, is_superuser=True)
    form2 = ProductForm(user=staff)
    assert "is_published" in form2.fields

def test_product_form_image_rejects_bad_extension(django_user_model):
    user = baker.make(django_user_model, is_superuser=True)
    cat = baker.make("catalog.Category")

    fake = SimpleUploadedFile("bad.gif", b"GIF89a", content_type="image/gif")
    form = ProductForm(
        data={"name": "ok", "description": "ok", "category": cat.pk, "price": "10.00"},
        files={"image": fake},
        user=user,
    )
    assert not form.is_valid()
    assert "image" in form.errors


def test_product_form_image_rejects_too_large(django_user_model):
    user = baker.make(django_user_model, is_superuser=True)
    cat = baker.make("catalog.Category")

    big = SimpleUploadedFile("big.jpg", b"x" * (5 * 1024 * 1024 + 10), content_type="image/jpeg")
    form = ProductForm(
        data={"name": "ok", "description": "ok", "category": cat.pk, "price": "10.00"},
        files={"image": big},
        user=user,
    )
    assert not form.is_valid()
    assert "image" in form.errors