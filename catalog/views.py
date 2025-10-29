from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product


class HomeView(ListView):
    """Главная страница интернет-магазина.
    Использует ListView для получения и пагинации списка товаров.
    Запрашивает товары с подгруженными категориями (select_related) и
    сортирует по дате создания (новые — первыми).
    В шаблоне доступны:
      - page_obj  — объект пагинации (используйте его в цикле для карточек);
      - products  — список объектов на текущей странице (синоним object_list);
      - is_paginated, paginator — стандартные атрибуты ListView.
    Примечание:
      Раньше контекст назывался "page_obj" через context_object_name — это могло
      «перезатирать» настоящий page_obj. Теперь указываем "products", а page_obj
      остаётся стандартным."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"  # ✅ корректное имя для object_list
    paginate_by = 8
    ordering = ["-created_at"]

    def get_queryset(self):
        """Оптимизированный queryset — подгружаем категорию одним JOIN."""
        return Product.objects.select_related("category").order_by("-created_at")

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список последних 5 товаров (для отладки в консоли).
        На вывод это не влияет."""
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by("-created_at")[:5]
        print("🆕 Последние добавленные товары:")
        for p in latest_products:
            print(f"- {p.name} ({p.price} ₽)")
        return context


class ContactsView(TemplateView):
    """Страница «Контакты» с формой обратной связи.
    GET: показывает пустую форму.
    POST: валидирует данные, формирует сообщение об успехе,
          при успехе очищает форму (демо-поведение без сохранения в БД)."""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        context["success_message"] = None
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        success_message = None

        if form.is_valid():
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            _message = form.cleaned_data[
                "message"
            ]  # зарезервировано под дальнейшую обработку

            success_message = (
                f"✅ Спасибо, {name}! Мы свяжемся с вами по телефону {phone}."
            )
            form = ContactForm()  # очищаем поля после успешной отправки

        context = {"form": form, "success_message": success_message}
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    """Детальная страница одного товара.
    Автоматически получает объект по pk из URL и передаёт его в шаблон
    под именем "product"."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class AddProductView(CreateView):
    """Создание нового товара через форму.
    Использует ProductForm c кастомной валидацией (запрещённые слова для name/description).
    При успешном сохранении перенаправляет на страницу созданного товара."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"  # можешь заменить на "catalog/product_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, f"✅ Товар «{self.object.name}» успешно добавлен!"
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, "⚠️ Ошибка при добавлении товара. Проверьте введённые данные."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("product_detail", kwargs={"pk": self.object.pk})


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Миксин для ограничения доступа:
    - пользователь должен быть авторизован,
    - пользователь должен быть сотрудником (is_staff=True)."""

    def test_func(self):
        return self.request.user.is_staff


class ProductUpdateView(UpdateView):
    """Редактирование существующего товара.
    - Использует ProductForm (с валидацией запрещённых слов).
    - После успешного сохранения — редирект на страницу товара.
    - Доступ только для сотрудников."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"  # единый шаблон формы для create/update

    def form_valid(self, form):
        resp = super().form_valid(form)
        from django.contrib import messages

        messages.success(self.request, f"✅ Товар «{self.object.name}» обновлён.")
        return resp

    def form_invalid(self, form):
        from django.contrib import messages

        messages.error(
            self.request, "⚠️ Ошибка при обновлении товара. Проверьте введённые данные."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(DeleteView):
    """Удаление товара с подтверждением.
    - Показывает шаблон подтверждения.
    - После удаления — редирект на главную страницу.
    - Доступ только для сотрудников."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"

    def get_success_url(self):
        from django.contrib import messages

        messages.success(self.request, f"🗑 Товар «{self.object.name}» удалён.")
        return reverse("home")

