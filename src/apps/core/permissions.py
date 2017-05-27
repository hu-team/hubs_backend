from rest_framework.permissions import BasePermission


class BasePersonPermission(BasePermission):

	def is_person(self, user):
		raise NotImplementedError()

	def has_permission(self, request, view):
		if not hasattr(request, 'user'):
			return False
		return self.is_person(request.user)

	def has_object_permission(self, request, view, obj):
		if not hasattr(request, 'user'):
			return False
		# TODO: Permission per models.
		return True


class IsTeacher(BasePersonPermission):
	def is_person(self, user):
		return user.is_teacher
