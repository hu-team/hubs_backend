from django.contrib import admin

from apps.core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">security</i>'
