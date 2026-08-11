from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import PostCreateForm, PostUpdateForm
from .models import Category, Post


class PostListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        return Post.published.select_related('author', 'category').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        page_obj = context['page_obj']
        context['paginator_range'] = page_obj.paginator.get_elided_page_range(page_obj.number)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class PostFromCategory(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        categories = self.category.get_descendants(include_self=True)
        return Post.published.filter(category__in=categories).select_related('author', 'category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Записи из категории: {self.category.title}'
        page_obj = context['page_obj']
        context['paginator_range'] = page_obj.paginator.get_elided_page_range(page_obj.number)
        return context


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'
    extra_context = {'title': 'Добавление статьи на сайт'}
    success_message = 'Запись была успешно создана!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    success_message = 'Запись была успешно обновлена!'

    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.info(self.request, 'Изменение статьи доступно только автору!')
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        return super().form_valid(form)
