from django.urls import path

from .views import PostCreateView, PostDetailView, PostFromCategory, PostListView, PostUpdateView

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('detail/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:slug>/', PostFromCategory.as_view(), name='post_from_category'),
]
