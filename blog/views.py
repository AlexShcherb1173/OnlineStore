from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib import messages
from .models import Post
from .forms import PostForm
from django.db.models import F

class PostListView(ListView):
    """Список постов. Для staff — все, для остальных — только опубликованные."""
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 12

    def get_queryset(self):
        qs = Post.objects.all().order_by("-created_at")
        user = self.request.user
        return qs if (user.is_authenticated and user.is_staff) else qs.filter(is_published=True)


class PostDetailView(DetailView):
    """Детальная страница поста с атомарным увеличением счётчика просмотров."""
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs if (user.is_authenticated and user.is_staff) else qs.filter(is_published=True)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(views_count=F("views_count") + 1)
        obj.refresh_from_db(fields=["views_count"])
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание поста."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.created_at = timezone.now()
        messages.success(self.request, f"✅ Пост «{form.instance.title}» успешно создан!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование поста.
    Доступно ЛЮБОМУ аутентифицированному пользователю (без проверки автора)."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, f"✏️ Пост «{form.instance.title}» обновлён.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление поста. Оставим только для staff, чтобы не потерять контент.
    Если нужно — снимите ограничение, убрав UserPassesTestMixin и test_func()."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Удаление доступно только сотрудникам (staff).")
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "🗑 Пост был удалён.")
        return super().delete(request, *args, **kwargs)