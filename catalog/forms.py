from django import forms
from django.core.exceptions import ValidationError
from django.forms import RadioSelect, CheckboxSelectMultiple
from .models import Product

# 🔒 Список запрещённых слов (используется в обоих валидаторах)
BANNED_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)

# ✅ константы для проверки изображений
ALLOWED_CONTENT_TYPES = ("image/jpeg", "image/png")
ALLOWED_FORMATS = ("JPEG", "PNG")
ALLOWED_EXTS = (".jpg", ".jpeg", ".png")
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 МБ


class BootstrapFormMixin:
    """Миксин для единообразной Bootstrap-стилизации всех полей формы.
    Делает следующее:
    - checkbox → class="form-check-input"
    - select / select multiple → class="form-select"
    - radio/checkbox списки (RadioSelect / CheckboxSelectMultiple) → корректные классы
    - file input → class="form-control"
    - остальные инпуты/textarea → class="form-control" """

    def _add_class(self, widget, class_name: str) -> None:
        # Безопасно наращиваем класс, даже если его ещё нет
        current = widget.attrs.get("class", "")
        widget.attrs["class"] = (current + " " + class_name).strip()

    def _init_bootstrap_widgets(self) -> None:
        for name, field in getattr(self, "fields", {}).items():
            widget = getattr(field, "widget", None)
            if widget is None:
                continue  # на всякий случай

            if isinstance(widget, RadioSelect):
                self._add_class(widget, "form-check")  # обертка ul/див
                # for отдельные input’ы radio класс добавляется на уровне рендеринга,
                # но базовый класс для списка всё равно полезен
                continue

            if isinstance(widget, CheckboxSelectMultiple):
                self._add_class(
                    widget, "form-check"
                )  # базовый класс для группы чекбоксов
                continue

                # 2) Чекбоксы (обычное BooleanField → CheckboxInput)
            input_type = getattr(widget, "input_type", None)
            if input_type == "checkbox":
                self._add_class(widget, "form-check-input")
                continue

            # 3) Select/SelectMultiple
            from django import forms as _forms

            if isinstance(widget, (_forms.Select, _forms.SelectMultiple)):
                self._add_class(widget, "form-select")
                continue

            # 4) Остальные поля: text/number/email/url/textarea/file и т. п.
            #    (в т.ч. ClearableFileInput)
            self._add_class(widget, "form-control")


class ContactForm(forms.Form, BootstrapFormMixin):
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
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ваш телефон"}
        ),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Ваше сообщение"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()


class ProductForm(forms.ModelForm, BootstrapFormMixin):
    """Форма для создания и редактирования продуктов.
    Особенности:
    - Показывает все пользовательские поля модели Product.
    - Содержит валидацию полей `name` и `description` на наличие запрещённых слов (без учёта регистра).
    - Проверяет, что цена продукта (`price`) не может быть отрицательной.
    - Использует Bootstrap-совместимые виджеты для удобного интерфейса."""

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите название"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Описание"}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "placeholder": "Цена"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_widgets()

    # ---------------------------
    # 🔸 Кастомные валидаторы
    # ---------------------------

    def _validate_banned(self, value: str) -> list[str]:
        """Возвращает список запрещённых слов, найденных в переданной строке (без учёта регистра)."""
        if not value:
            return []
        low = value.lower()
        return [w for w in BANNED_WORDS if w in low]

    def clean_name(self):
        """Проверяет поле `name` на наличие запрещённых слов."""
        name = self.cleaned_data.get("name") or ""
        hits = self._validate_banned(name)
        if hits:
            raise forms.ValidationError(
                f"❌ В названии обнаружены запрещённые слова: {', '.join(hits)}."
            )
        return name

    def clean_description(self):
        """Проверяет поле `description` на наличие запрещённых слов."""
        desc = self.cleaned_data.get("description") or ""
        hits = self._validate_banned(desc)
        if hits:
            raise forms.ValidationError(
                f"⚠️ В описании обнаружены запрещённые слова: {', '.join(hits)}."
            )
        return desc

    def clean_price(self):
        """Проверяет, что цена продукта не отрицательная.
        Raises:
            ValidationError: если цена меньше нуля.
        Returns:
            float: корректное значение цены."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("⚠️ Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        """Валидирует загружаемое изображение:
        - формат: только JPEG или PNG;
        - размер: не более 5 МБ;
        - проверка реального формата через Pillow (а не только по расширению)."""
        img = self.cleaned_data.get("image")
        if not img:
            return img  # изображение не обязательно — пропускаем

        # 1) Проверка размера
        if img.size and img.size > MAX_IMAGE_BYTES:
            raise ValidationError("Размер файла превышает 5 МБ.")

        # 2) Быстрая проверка content_type/расширения
        content_type = getattr(img, "content_type", "") or ""
        name_lower = (img.name or "").lower()
        if content_type and content_type not in ALLOWED_CONTENT_TYPES:
            raise ValidationError("Допустимы только изображения JPEG или PNG.")
        if not name_lower.endswith(ALLOWED_EXTS):
            raise ValidationError("Расширение файла должно быть .jpg, .jpeg или .png.")

        # 3) Надёжная проверка формата через Pillow
        try:
            from PIL import Image

            pos = img.file.tell() if hasattr(img.file, "tell") else 0
            img.file.seek(0)
            with Image.open(img.file) as pil_img:
                pil_img.verify()  # проверка целостности
                if pil_img.format not in ALLOWED_FORMATS:
                    raise ValidationError("Файл не является валидным JPEG или PNG.")
        except ValidationError:
            raise
        except Exception:
            raise ValidationError("Некорректное изображение или повреждённый файл.")
        finally:
            # возвращаем курсор файла на место, чтобы Django смог перечитать поток
            try:
                img.file.seek(pos)
            except Exception:
                pass

        return img
