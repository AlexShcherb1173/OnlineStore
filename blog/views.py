from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib import messages
from .models import Post


class PostListView(ListView):
    """CBV для отображения списка блоговых записей.
    Отображает только опубликованные посты."""

    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 6  # постраничный вывод по 6 постов

    def get_queryset(self):
        """Возвращает только опубликованные посты, отсортированные по дате."""
        return Post.objects.filter(is_published=True).order_by("-created_at")


class PostDetailView(DetailView):
    """CBV для отображения одной блоговой записи с увеличением счётчика просмотров."""

    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        """При каждом просмотре увеличивает количество просмотров."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class PostCreateView(CreateView):
    """CBV для создания нового поста."""

    model = Post
    fields = ["title", "content", "preview", "is_published"]
    template_name = "post_form.html"

    def form_valid(self, form):
        """Добавляет сообщение при успешном создании поста."""
        form.instance.created_at = timezone.now()
        messages.success(
            self.request, f"✅ Пост «{form.instance.title}» успешно создан!"
        )
        return super().form_valid(form)

    def get_success_url(self):
        """После создания возвращает на список постов."""
        return reverse_lazy("blog:post_list")


class PostUpdateView(UpdateView):
    """CBV для редактирования поста."""

    model = Post
    fields = ["title", "content", "preview", "is_published"]
    template_name = "post_form.html"

    def form_valid(self, form):
        messages.success(self.request, f"✏️ Пост «{form.instance.title}» обновлён.")
        return super().form_valid(form)

    def get_success_url(self):
        # Перенаправляем на страницу только что созданного поста
        return reverse_lazy("blog:post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(DeleteView):
    """CBV для удаления поста с подтверждением."""

    model = Post
    template_name = "post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def delete(self, request, *args, **kwargs):
        messages.warning(request, "🗑 Пост был удалён.")
        return super().delete(request, *args, **kwargs)
