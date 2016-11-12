from django.contrib import admin
from bot.models import UserPrefs

admin.site.site_header = 'boMOt Admin site'


class UserPrefsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ('user_id', 'fav_movies')
admin.site.register(UserPrefs, UserPrefsAdmin)
