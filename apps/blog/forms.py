from django import forms

from .models import Post, Comment


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'image', 'fixed', 'excerpt', 'description', 'status')
        widgets = {
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


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 30,
                'rows': 5,
                'class': 'form-control',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = ''
