from django.urls import path

from .views import (
    PostByTagListView,
    PostCreateView,
    PostDetailView,
    PostFromCategory,
    PostListView,
    PostUpdateView,
    comment_create,
)

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostFromCategory.as_view(), name='post_from_category'),
    path('post/<int:post_id>/comment/', comment_create, name='comment_create'),
    path('post/tags/<slug:tag>/', PostByTagListView.as_view(), name='post_by_tags'),
]
