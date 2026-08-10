from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import ProfileUpdateForm, UserLoginForm, UserRegisterForm, UserUpdateForm
from .models import Profile

User = get_user_model()


class ProfileOwnerDetailView(LoginRequiredMixin, DetailView):  # Profile only, т.к. User итак в контексте
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        return context


class ProfileOtherDetailView(DetailView):  # Profile only, т.к. User итак в контексте
    model = Profile
    template_name = 'accounts/profile.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Профиль пользователя: {self.object.user.username}'
        return context


@login_required
def profile_edit(request):  # Profile + User
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Профиль успешно отредактирван')
            return redirect('profile_owner')
        else:
            messages.error(request, 'Проверьте правильность заполнения формы')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': f'Редактирование аккаунта : {request.user.username}',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/profile_edit.html', context)


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    extra_context = {'title': 'Регистрация на сайте'}
    success_message = 'Вы успешно зарегистрировались. Вход выполнен!'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    redirect_authenticated_user = True
    authentication_form = UserLoginForm
    template_name = 'accounts/user_login.html'
    extra_context = {'title': 'Авторизация на сайте'}
    success_message = 'Добро пожаловать на сайт!'
