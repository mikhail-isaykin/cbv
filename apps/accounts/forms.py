from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(
                attrs={'class': 'form-control mb-1'},
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control mb-1'},
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control mb-1'},
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control mb-1'},
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Email адрес должен быть уникальным')
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'bio', 'avatar')
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'class': 'form-control mb-1',
                    'type': 'date',
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control mb-1',
                    'rows': 4,
                }
            ),
            'avatar': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control mb-1',
                }
            ),
        }


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Придумайте свой логин', 'class': 'form-control mb-1', 'autocomplete': 'off'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Введите свой email', 'class': 'form-control mb-1', 'autocomplete': 'off'}
            ),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Ваше имя', 'class': 'form-control mb-1', 'autocomplete': 'off'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Ваша фамилия', 'class': 'form-control mb-1', 'autocomplete': 'off'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'placeholder': 'Придумайте свой пароль', 'class': 'form-control', 'autocomplete': 'new-password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Повторите придуманный пароль', 'class': 'form-control', 'autocomplete': 'new-password'}
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Логин пользователя',
                'autocomplete': 'username',
            }
        )
        self.fields['username'].label = 'Логин'
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Пароль пользователя',
                'autocomplete': 'current-password',
            }
        )
