from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView, UpdateView
from django.conf import settings

from .forms import UserRegistrationForm, EmailAuthenticationForm, ProfileForm, DeleteAccountForm

User = get_user_model()

class RegisterView(FormView):
    """
    Регистрация пользователя:
    - сохраняет пользователя;
    - аутентифицирует по email+password через кастомный backend;
    - при необходимости логинит с явным указанием backend;
    - отправляет приветственное письмо;
    - редиректит на главную.
    """
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        # 1) Сохраняем пользователя (форма уже хеширует пароль)
        user = form.save()

        # 2) Аутентификация через кастомный email backend
        email = user.email
        raw_password = form.cleaned_data.get("password1")
        authenticated_user = authenticate(self.request, email=email, password=raw_password)

        if authenticated_user is not None:
            # authenticate() проставил backend → login пройдёт без ошибок
            login(self.request, authenticated_user)
        else:
            # Фолбэк: явно указываем backend, чтобы избежать ValueError про multiple backends
            login(self.request, user, backend="users.backends.EmailAuthBackend")

        # 3) Письмо приветствия на адрес, введённый при регистрации (user.email)
        try:
            send_mail(
                subject="Добро пожаловать в SkyStore! 🎉",
                message=(
                    f"Здравствуйте, {user.email}!\n\n"
                    "Спасибо за регистрацию в SkyStore. Рады видеть вас 😊\n\n"
                    "— Команда SkyStore"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,  # адрес отправителя из .env
                recipient_list=[user.email],  # адрес получателя из формы регистрации
                fail_silently=False,
            )
        except Exception as e:
            messages.warning(self.request, f"⚠️ Не удалось отправить письмо: {e}")

        messages.success(self.request, "✅ Регистрация успешна! Добро пожаловать 👋")
        return super().form_valid(form)


class LoginView(FormView):
    """Авторизация по email и паролю."""
    template_name = "users/login.html"
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()  # внутри формы мы уже вызвали authenticate()
        # На всякий случай: если у user нет backend (редко), логиним через наш backend
        try:
            login(self.request, user)
        except Exception:
            login(self.request, user, backend="users.backends.EmailAuthBackend")

        messages.success(self.request, "Вы вошли в аккаунт.", extra_tags="auth")
        next_url = self.request.GET.get("next")
        return redirect(next_url or reverse("catalog:home"))


class LogoutView(LoginRequiredMixin, TemplateView):
    """Выход с редиректом на главную."""
    template_name = "users/logged_out.html"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Вы вышли из аккаунта.", extra_tags="auth")
        return redirect("catalog:home")

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование собственного профиля."""
    model = User
    form_class = ProfileForm
    template_name = "users/profile_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлён ✅")
        return super().form_valid(form)

    def get_success_url(self):
        # после сохранения вернёмся на эту же страницу
        return reverse_lazy("users:profile_edit")


class AccountDeleteView(LoginRequiredMixin, FormView):
    """Удаление аккаунта с дополнительным подтверждением."""
    template_name = "users/profile_confirm_delete.html"
    form_class = DeleteAccountForm
    success_url = reverse_lazy("catalog:home")  # поменяйте при необходимости

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        email = user.email
        # выход и удаление
        logout(self.request)
        user.delete()
        messages.warning(self.request, f"Аккаунт {email} удалён. Нам будет вас не хватать 😢")
        return super().form_valid(form)
