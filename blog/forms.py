from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "preview", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Заголовок поста"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Содержимое "
            }),
            "preview": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "is_published": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }