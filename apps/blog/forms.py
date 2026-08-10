from django import forms

from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'image', 'fixed', 'excerpt', 'description', 'status')
        widgets = {  #noqa: RUF012
            'category': forms.Select(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Заголовок статьи',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
            }),
            'fixed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'autocomplete': 'off',
            }),
            'excerpt': forms.TextInput(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': 'Краткое описание',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'autocomplete': 'off',
                'rows': 8,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'autocomplete': 'off',
            }),
        }


class PostUpdateForm(PostCreateForm):
    """
    Форма обновления статьи на сайте
    """
