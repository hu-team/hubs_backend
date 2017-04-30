from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
	icon = '<i class="material-icons">security</i>'
	list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser')
	list_filter = ('is_superuser',)
	search_fields = ('username', 'first_name', 'last_name', 'email')
