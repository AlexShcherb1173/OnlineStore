from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя по email и паролю.
    Валидирует уникальность email и совпадение паролей.
    """

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
    )

    class Meta:
        model = User
        fields = ["email", "avatar", "phone", "country"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "you@example.com"}
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "+7..."}
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Страна"}
            ),
        }

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Пароли не совпадают.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # если у модели есть username и он обязательный — можно подставить email
        if hasattr(user, "username") and not user.username:
            user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"].lower()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    """Форма авторизации по email и паролю."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "autocomplete": "email"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "current-password"}
        ),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = (cleaned.get("email") or "").lower()
        password = cleaned.get("password")
        if email and password:
            # Работает если USERNAME_FIELD='email' или настроен кастомный backend (см. ниже).
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise ValidationError("Неверный email или пароль.")
            if not self.user.is_active:
                raise ValidationError("Аккаунт не активен.")
        return cleaned

    def get_user(self):
        return self.user


class ProfileForm(forms.ModelForm):
    """Редактирование профиля текущего пользователя."""

    class Meta:
        model = User
        # Если в вашей модели нет avatar — уберите его из списка полей.
        fields = (
            ["first_name", "last_name", "email", "avatar"]
            if hasattr(User, "avatar")
            else ["first_name", "last_name", "email"]
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            # avatar рисуем стандартным виджетом file input
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        qs = User.objects.exclude(pk=self.instance.pk).filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("Пользователь с таким e-mail уже существует.")
        return email


class DeleteAccountForm(forms.Form):
    """Подтверждение удаления: ввод e-mail + текущего пароля + галочка-согласие."""

    email = forms.EmailField(
        label="Ваш e-mail", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Текущий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    agree = forms.BooleanField(
        label="Я понимаю, что удаление аккаунта необратимо",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("email")
        password = cleaned.get("password")

        if email and email.lower() != (self.user.email or "").lower():
            self.add_error("email", "E-mail не совпадает с адресом вашего аккаунта.")

        if password:
            # аутентифицируемся через ваш email backend
            u = authenticate(None, email=self.user.email, password=password)
            if u is None:
                self.add_error("password", "Неверный пароль.")
        return cleaned
