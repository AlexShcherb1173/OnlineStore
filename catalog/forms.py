from django import forms
from .models import Product


class ContactForm(forms.Form):
    """Форма обратной связи для страницы "Контакты".
    Используется для ввода имени пользователя, его контактного телефона
    и сообщения. Все поля стилизованы с помощью Bootstrap (form-control)."""

    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ваше имя"}
        ),
    )
    """Поле для ввода имени пользователя.
        - label: отображаемая метка поля ("Имя")
        - max_length: ограничение на 100 символов
        - widget: HTML <input type="text"> со стилем Bootstrap и placeholder"""

    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ваш телефон"}
        ),
    )
    """Поле для ввода номера телефона.
        - label: отображаемая метка поля ("Телефон")
        - max_length: ограничение на 20 символов
        - widget: HTML <input type="text"> со стилем Bootstrap и placeholder"""

    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Ваше сообщение"}
        ),
    )
    """Поле для ввода текста сообщения.
        - label: отображаемая метка поля ("Сообщение")
        - widget: HTML <textarea> со стилем Bootstrap и placeholder"""


class ProductForm(forms.ModelForm):
    """Форма для добавления нового товара.
    Поля соответствуют модели Product."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Описание"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }
