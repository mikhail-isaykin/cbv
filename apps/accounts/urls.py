from django.contrib.auth import views as auth_views
from django.urls import path

from .views import ProfileOtherDetailView, ProfileOwnerDetailView, UserLoginView, UserRegisterView, profile_edit

urlpatterns = [
    path('profile/', ProfileOwnerDetailView.as_view(), name='profile_owner'),
    path('profile/<slug:slug>', ProfileOtherDetailView.as_view(), name='profile_other'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
