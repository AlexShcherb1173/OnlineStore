from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView
from django.conf import settings

from .forms import UserRegistrationForm, EmailAuthenticationForm


class RegisterView(FormView):
    """Регистрация пользователя:
    - сохраняет пользователя,
    - логинит,
    - шлёт приветственное письмо,
    - редиректит на главную.
    """
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        # приветственное письмо
        try:
            send_mail(
                subject="Добро пожаловать в SkyStore! 🎉",
                message=(
                    f"Здравствуйте, {getattr(user, 'email', 'пользователь')}!\n\n"
                    "Спасибо за регистрацию в SkyStore. Рады видеть вас 😊"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # чтобы не ломать регистрацию, просто покажем предупреждение
            messages.warning(self.request, f"Письмо не отправлено: {e}")

        messages.success(self.request, "Регистрация успешна! Добро пожаловать 👋")
        return super().form_valid(form)


class LoginView(FormView):
    """Авторизация по email и паролю."""
    template_name = "users/login.html"
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Вы вошли в аккаунт.")
        next_url = self.request.GET.get("next")
        return redirect(next_url or reverse("home"))


class LogoutView(LoginRequiredMixin, TemplateView):
    """Выход с редиректом на главную."""
    template_name = "users/logged_out.html"

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "Вы вышли из аккаунта.")
        return redirect("home")
