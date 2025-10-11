from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from catalog.forms import ContactForm, ProductForm
from catalog.models import Product


def home_view(request):
    """Контроллер для главной страницы.
    Получает список всех продуктов из БД и
    передаёт их в шаблон для отображения.
    Также выбирает последние 5 для консоли."""
    products = Product.objects.select_related("category").all().order_by("-created_at")
    # latest_products = products[:5]
    #
    # print("🆕 Последние добавленные продукты:")
    # for p in latest_products:
    #     print(f"- {p.name} ({p.price} ₽)")
    #
    # return render(request, "home.html", {"products": products})
    paginator = Paginator(products, 8)  # по 8 товаров на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "home.html", {"page_obj": page_obj})


def contacts_view(request):
    """Контроллер (view) для страницы "Контакты" с формой обратной связи.
    Поведение:
    - Если запрос GET → отображает пустую форму.
    - Если запрос POST → обрабатывает отправленные данные формы.
    - При успешной валидации формы формирует success_message и очищает поля.
    - Данные формы можно расширить обработкой (сохранение в БД или отправка email).
    Аргументы:
        request (HttpRequest): объект запроса от клиента.
    Контекст:
        form (ContactForm): экземпляр формы (пустой или с введёнными данными).
        success_message (str | None): сообщение об успешной отправке формы
            или None, если форма не была отправлена или содержит ошибки.
    Возвращает:
        HttpResponse: отрендеренный шаблон contacts.html с формой и сообщением."""
    success_message = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику (сохранение в БД или отправка email)
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            # Для примера: просто показываем сообщение об успехе
            success_message = (
                f"✅ Спасибо, {name}! Мы свяжемся с вами по телефону {phone}."
            )
            form = ContactForm()  # очищаем форму после отправки
    else:
        form = ContactForm()

    return render(
        request, "contacts.html", {"form": form, "success_message": success_message}
    )


def product_detail_view(request, pk):
    """Контроллер для отображения одного товара.
    Принимает pk, получает объект Product из базы данных
    и рендерит шаблон с подробной информацией."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def add_product_view(request):
    """Контроллер для добавления нового товара.
    Обрабатывает GET (форма) и POST (сохранение)."""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"✅ Товар '{product.name}' успешно добавлен!")
            return redirect("home")
        else:
            messages.error(
                request, "⚠️ Ошибка при добавлении товара. Проверьте введённые данные."
            )
    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})
