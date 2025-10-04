from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
def home_view(request):
    """Контроллер для главной страницы"""
    return render(request, "home.html")


def contacts_view(request):
    success_message = None

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику (сохранение в БД или отправка email)
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            # Для примера: просто показываем сообщение об успехе
            success_message = f"✅ Спасибо, {name}! Мы свяжемся с вами по телефону {phone}."
            form = ContactForm()  # очищаем форму после отправки
    else:
        form = ContactForm()

    return render(request, "contacts.html", {
        "form": form,
        "success_message": success_message
    })
