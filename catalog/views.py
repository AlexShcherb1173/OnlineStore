from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import get_object_or_404, redirect
from django.views import View
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
from catalog.models import Product, Category
from catalog.services import get_products_by_category
from catalog.cache_utils import invalidate_home_products


class HomeView(ListView):
    """Главная страница интернет-магазина — с низкоуровневым кешированием списка продуктов."""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 8
    ordering = ["-created_at"]

    def get_queryset(self):
        """Возвращает список продуктов с учётом кеширования."""
        user = self.request.user
        is_staff = user.is_authenticated and user.is_staff

        # ключ для кэша зависит от роли пользователя
        cache_key = f"home:products:{'staff' if is_staff else 'public'}"
        cache_ttl = getattr(settings, "CACHE_TTL", 300)  # 5 минут по умолчанию

        products = None
        if getattr(settings, "CACHE_ENABLED", False):
            products = cache.get(cache_key)

        if products is None:
            print("🧱 Кэш пуст — загружаем продукты из базы")
            qs = Product.objects.select_related("category").order_by("-created_at")
            if not is_staff:
                qs = qs.filter(is_published=True)

            # превращаем QuerySet в list, чтобы не было повторных SQL-запросов
            products = list(qs)

            if getattr(settings, "CACHE_ENABLED", False):
                cache.set(cache_key, products, cache_ttl)
                print(f"✅ Кэш обновлён: {cache_key}")
        else:
            print(f"⚡ Используем продукты из кэша: {cache_key}")

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Просто отладочная выдача последних 5 товаров (не влияет на шаблон)
        latest_products = Product.objects.order_by("-created_at")[:5]
        print("🆕 Последние добавленные товары:")
        for p in latest_products:
            print(f"- {p.name} ({p.price} ₽)")
        # Добавляем список всех категорий для кнопок
        context["categories"] = Category.objects.all().order_by("name")
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
    """Обычным пользователям доступна только опубликованная карточка.
    Staff видит любую."""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        return qs.filter(is_published=True)


class AddProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание товара — только для пользователей с правом add_product."""

    model = Product
    form_class = ProductForm
    template_name = (
        "catalog/add_product.html"  # можешь заменить на "catalog/product_form.html"
    )
    permission_required = "catalog.add_product"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # ← передаём пользователя в форму
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        responce = super().form_valid(form)
        invalidate_home_products()
        messages.success(
            self.request, f"✅ Товар «{self.object.name}» успешно добавлен!"
        )
        return responce

    def form_invalid(self, form):
        messages.error(
            self.request, "⚠️ Ошибка при добавлении товара. Проверьте введённые данные."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class OwnerRequiredMixin(UserPassesTestMixin):
    """Доступ разрешён только владельцу (или суперюзеру)."""

    def test_func(self):
        obj = getattr(self, "object", None) or self.get_object()
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or obj.owner_id == user.id)

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на выполнение этого действия.")
        return super().handle_no_permission()


class OwnerOrModeratorRequiredMixin(UserPassesTestMixin):
    """Удалять может владелец или пользователь с правом delete_product (модератор/суперюзер)."""

    def test_func(self):
        obj = getattr(self, "object", None) or self.get_object()
        user = self.request.user
        if not user.is_authenticated:
            return False
        return (
            (obj.owner_id == user.id)
            or user.is_superuser
            or user.has_perm("catalog.delete_product")
        )

    def handle_no_permission(self):
        messages.error(
            self.request, "Удалять товар может только владелец или модератор."
        )
        return super().handle_no_permission()


# class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
#     """Миксин для ограничения доступа:
#     - пользователь должен быть авторизован,
#     - пользователь должен быть сотрудником (is_staff=True)."""
#
#     def test_func(self):
#         return self.request.user.is_staff


class ProductUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    """Редактирование — только с правом change_product."""

    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"  # единый шаблон формы для create/update
    # permission_required = "catalog.change_product"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # ← передаём пользователя в форму
        return kwargs

    def form_valid(self, form):
        resp = super().form_valid(form)
        invalidate_home_products()
        messages.success(
            self.request,
            f"✅ Товар «{self.object.name}» обновлён.",
            extra_tags="catalog",
        )
        return resp

    def form_invalid(self, form):

        messages.error(
            self.request,
            "⚠️ Ошибка при обновлении товара. Проверьте введённые данные.",
            extra_tags="catalog",
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorRequiredMixin, DeleteView):
    """Удаление — только с правом delete_product."""

    model = Product
    template_name = "catalog/product_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, f"🗑 Товар «{self.object.name}» удалён.")
        invalidate_home_products()
        return reverse("catalog:home")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Снять с публикации — только с кастомным правом can_unpublish_product."""

    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save(update_fields=["is_published"])
        invalidate_home_products()
        messages.info(request, f"Публикация товара «{product.name}» отменена.")
        return redirect(product.get_absolute_url())


class OwnerRequiredMixin(UserPassesTestMixin):
    """Доступ разрешён только владельцу (или суперюзеру)."""

    def test_func(self):
        obj = getattr(self, "object", None) or self.get_object()
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or obj.owner_id == user.id)

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на выполнение этого действия.")
        return super().handle_no_permission()


class CategoryProductsView(TemplateView):
    """Представление для отображения всех товаров в выбранной категории."""

    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, pk=category_id)

        context["category"] = category
        context["products"] = get_products_by_category(category.id)
        return context
