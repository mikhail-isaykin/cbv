from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CommentCreateForm, PostCreateForm, PostUpdateForm
from .models import Category, Post, RuTag


class PostListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

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
        context['comments'] = self.object.comments.all()
        context['form'] = CommentCreateForm()
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


@login_required
@require_POST
def comment_create(request, post_id):
    form = CommentCreateForm(request.POST)
    if not form.is_valid():
        print(form.errors)
        return render(request, 'blog/includes/_comment_errors.html', {'form': form}, status=400)

    comment = form.save(commit=False)
    comment.post_id = post_id
    comment.author = request.user
    comment.parent = form.cleaned_data.get('parent')
    comment.save()

    return render(
        request,
        'blog/includes/_comment.html',
        {
            'comment': comment,
            'post': comment.post,
            'form': CommentCreateForm(),
            'required': True,
        },
    )


class PostByTagListView(PostListView):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.tag = get_object_or_404(RuTag, slug=kwargs['tag'])

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи по тегу: {self.tag.name}'
        return context
