from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'birth_date')
    list_filter = ('birth_date',)
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('slug',)
    ordering = ('user',)
    autocomplete_fields = ('user',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ('slug',)
        return ()
