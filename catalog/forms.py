from django import forms


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
