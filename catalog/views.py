from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from catalog.forms import ContactForm, ProductForm
from catalog.models import Product


class HomeView(ListView):
    """Представление для главной страницы интернет-магазина.

    Использует класс `ListView` для отображения списка товаров с пагинацией.
    Выполняет ORM-запрос для получения всех продуктов из базы данных,
    сортируя их по дате создания (новые — первыми).

    Основные функции:
    - Получает все товары с помощью ORM-запроса `Product.objects.select_related("category")`
      для оптимизации (один SQL-запрос с подгрузкой категорий).
    - Проводит постраничный вывод (`paginate_by = 8`).
    - Выводит последние 5 добавленных товаров в консоль (для отладки).
    - Рендерит шаблон `home.html` и передаёт в контекст объект `page_obj`
      для итерации в шаблоне.

    Атрибуты класса:
        model (Model): модель, с которой работает контроллер (`Product`).
        template_name (str): путь к шаблону, который будет отображён.
        context_object_name (str): имя переменной, доступной в шаблоне.
        paginate_by (int): количество элементов на странице.
        ordering (list[str]): порядок сортировки (по дате создания, убывание).

    Контекст:
        page_obj (Page): объект страницы с товарами."""

    model = Product
    template_name = "home.html"
    context_object_name = "page_obj"
    paginate_by = 8
    ordering = ["-created_at"]

    def get_queryset(self):
        """Возвращает оптимизированный queryset с подгруженными категориями."""
        return Product.objects.select_related("category").order_by("-created_at")

    def get_context_data(self, **kwargs):
        """Добавляет в контекст список последних 5 товаров (для отладки)."""
        context = super().get_context_data(**kwargs)
        latest_products = Product.objects.order_by("-created_at")[:5]
        print("🆕 Последние добавленные товары:")
        for p in latest_products:
            print(f"- {p.name} ({p.price} ₽)")
        return context


class ContactsView(TemplateView):
    """Представление для страницы "Контакты" с формой обратной связи.

    Использует `TemplateView`, поскольку шаблон в основном статический,
    но при этом содержит форму `ContactForm`, которую пользователь может отправить.

    Поведение:
    - При `GET`-запросе отображает страницу с пустой формой.
    - При `POST`-запросе обрабатывает введённые данные, валидирует форму и,
      если всё успешно, формирует сообщение об успехе (без сохранения в БД).

    Атрибуты класса:
        template_name (str): шаблон страницы (`contacts.html`).

    Контекст:
        form (ContactForm): форма для заполнения пользователем.
        success_message (str | None): сообщение об успешной отправке данных.

    Возвращает:
        HttpResponse: отрендеренный шаблон с формой и сообщением."""

    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        """Добавляет форму в контекст при первичном отображении страницы."""
        context = super().get_context_data(**kwargs)
        context["form"] = ContactForm()
        context["success_message"] = None
        return context

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос, валидирует форму и возвращает результат."""
        form = ContactForm(request.POST)
        success_message = None

        if form.is_valid():
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            success_message = (
                f"✅ Спасибо, {name}! Мы свяжемся с вами по телефону {phone}."
            )
            form = ContactForm()  # очищаем поля после успешной отправки

        context = {"form": form, "success_message": success_message}
        return self.render_to_response(context)


class ProductDetailView(DetailView):
    """Представление для отображения детальной страницы одного товара.

    Использует `DetailView`, который автоматически получает объект по его первичному ключу (pk).
    После получения товара передаёт объект в шаблон `product_detail.html`.

    Атрибуты класса:
        model (Model): модель товара (`Product`).
        template_name (str): шаблон страницы.
        context_object_name (str): имя переменной для объекта в шаблоне (`product`).

    Контекст:
        product (Product): объект выбранного товара, доступный в шаблоне.

    Пример использования в шаблоне:
        {{ product.name }}
        {{ product.description }}
        <img src="{{ product.image.url }}" alt="{{ product.name }}">"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class AddProductView(CreateView):
    """Представление для добавления нового товара через форму.

    Использует `CreateView` для генерации формы на основе модели `Product`.
    Поддерживает загрузку изображений, обработку ошибок и вывод сообщений
    о результате операции через `django.contrib.messages`.

    Поведение:
    - При `GET` — отображает пустую форму.
    - При `POST` — создаёт новый объект `Product` в базе данных при успешной валидации.

    Атрибуты класса:
        model (Model): модель `Product`.
        form_class (Form): форма `ProductForm` для ввода данных.
        template_name (str): шаблон страницы (`add_product.html`).
        success_url (str): URL для перенаправления после успешного добавления.

    Контекст:
        form (ProductForm): форма добавления нового товара.

    Пример успешного добавления:
        ✅ Товар 'Ноутбук ASUS VivoBook' успешно добавлен!"""

    model = Product
    form_class = ProductForm
    template_name = "add_product.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        """Сохраняет товар и отображает сообщение об успехе."""
        product = form.save()
        messages.success(self.request, f"✅ Товар '{product.name}' успешно добавлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """Выводит сообщение об ошибке, если форма не прошла валидацию."""
        messages.error(
            self.request,
            "⚠️ Ошибка при добавлении товара. Проверьте введённые данные.",
        )
        return super().form_invalid(form)


# FBV version of contollers
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from catalog.forms import ContactForm, ProductForm
# from catalog.models import Product
#
#
# def home_view(request):
#     """Контроллер для главной страницы.
#     Получает список всех продуктов из БД и
#     передаёт их в шаблон для отображения.
#     Также выбирает последние 5 для консоли."""
#     products = Product.objects.select_related("category").all().order_by("-created_at")
#     # latest_products = products[:5]
#     #
#     # print("🆕 Последние добавленные продукты:")
#     # for p in latest_products:
#     #     print(f"- {p.name} ({p.price} ₽)")
#     #
#     # return render(request, "home.html", {"products": products})
#     paginator = Paginator(products, 8)  # по 8 товаров на страницу
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, "home.html", {"page_obj": page_obj})
#
#
# def contacts_view(request):
#     """Контроллер (view) для страницы "Контакты" с формой обратной связи.
#     Поведение:
#     - Если запрос GET → отображает пустую форму.
#     - Если запрос POST → обрабатывает отправленные данные формы.
#     - При успешной валидации формы формирует success_message и очищает поля.
#     - Данные формы можно расширить обработкой (сохранение в БД или отправка email).
#     Аргументы:
#         request (HttpRequest): объект запроса от клиента.
#     Контекст:
#         form (ContactForm): экземпляр формы (пустой или с введёнными данными).
#         success_message (str | None): сообщение об успешной отправке формы
#             или None, если форма не была отправлена или содержит ошибки.
#     Возвращает:
#         HttpResponse: отрендеренный шаблон contacts.html с формой и сообщением."""
#     success_message = None
#
#     if request.method == "POST":
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             # Здесь можно добавить логику (сохранение в БД или отправка email)
#             name = form.cleaned_data["name"]
#             phone = form.cleaned_data["phone"]
#             message = form.cleaned_data["message"]
#
#             # Для примера: просто показываем сообщение об успехе
#             success_message = (
#                 f"✅ Спасибо, {name}! Мы свяжемся с вами по телефону {phone}."
#             )
#             form = ContactForm()  # очищаем форму после отправки
#     else:
#         form = ContactForm()
#
#     return render(
#         request, "contacts.html", {"form": form, "success_message": success_message}
#     )
#
#
# def product_detail_view(request, pk):
#     """Контроллер для отображения одного товара.
#     Принимает pk, получает объект Product из базы данных
#     и рендерит шаблон с подробной информацией."""
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, "product_detail.html", {"product": product})
#
#
# def add_product_view(request):
#     """Контроллер для добавления нового товара.
#     Обрабатывает GET (форма) и POST (сохранение)."""
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save()
#             messages.success(request, f"✅ Товар '{product.name}' успешно добавлен!")
#             return redirect("home")
#         else:
#             messages.error(
#                 request, "⚠️ Ошибка при добавлении товара. Проверьте введённые данные."
#             )
#     else:
#         form = ProductForm()
#
#     return render(request, "add_product.html", {"form": form})
