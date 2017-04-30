from django.contrib import admin

from apps.school.models import Student, Teacher, Counselor


@admin.register(Student, Teacher, Counselor)
class PersonAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">person</i>'
