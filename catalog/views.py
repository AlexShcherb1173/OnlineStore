from django.shortcuts import render
from .forms import ContactForm


# Create your views here.
def home_view(request):
    """Контроллер для главной страницы
    Аргументы: request (HttpRequest): объект запроса от клиента.
    Возвращает: HttpResponse: отрендеренный шаблон home.html."""

    return render(request, "home.html")


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
