from django.contrib import admin

from apps.school.models import Student, Teacher, Counselor, Course, Group, Lesson


@admin.register(Student, Teacher, Counselor)
class PersonAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">person</i>'
	list_display = ('full_name', 'get_email', 'get_username')
	search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')

	def get_email(self, obj):
		return obj.user.email

	def get_username(self, obj):
		return obj.user.username

	get_email.short_description = 'Email'
	get_username.short_description = 'Username'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">book</i>'
	list_display = ('code', 'school_year')
	list_filter = ('school_year',)
	search_fields = ('code', 'school_year')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">group</i>'
	list_display = ('code', 'school_year')
	list_filter = ('school_year',)
	search_fields = ('code', 'school_year')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">schedule</i>'
	list_display = ('course', 'teacher', 'group', 'get_school_year', 'start', 'end')
	list_filter = ('course__school_year', 'teacher', 'group', 'course')

	def get_school_year(self, obj):
		return obj.course.school_year

	get_school_year.short_description = 'School year'
