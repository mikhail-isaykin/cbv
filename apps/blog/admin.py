from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category, Post, Comment


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    #list_display = ('tree_actions', 'indented_title', 'posts_count')
    #list_display_links = ('indented_title',)
    search_fields = ('title', 'description')
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('slug',)
        return ()
    
    @admin.display(description='Posts')
    def posts_count(self, obj):
        return obj.posts.count()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'status', 'fixed', 'created_at', 'updated_at')
    list_filter = ('status', 'fixed', 'category', 'created_at')
    search_fields = ('title', 'description', 'excerpt')
    autocomplete_fields = ('category',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('fixed', 'status')
    date_hierarchy = 'created_at'
    exclude = ('author', 'updater')
    
    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('slug',)
        return ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        else:
            obj.updater = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(DjangoMpttAdmin):
    list_display = ('author', 'post', 'text', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('text', 'author__username')