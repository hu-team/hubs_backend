from rest_framework.permissions import BasePermission, IsAuthenticated


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


class StudentNotAllowed(IsAuthenticated):

	def has_permission(self, request, view):
		if request.user.is_student:
			return False
		return True


class StudentReadOnlyAndPost(IsAuthenticated):

	NOT_METHODS = ['DELETE', 'PATCH', 'PUT']

	def has_permission(self, request, view):
		if request.method in self.NOT_METHODS and request.user.is_student:
			return False
		return True


class ReadOnlyOrWriteAccess(IsAuthenticated):

	NOT_METHODS = ['POST', 'DELETE', 'PATCH', 'PUT']

	def has_permission(self, request, view):
		if request.method in self.NOT_METHODS and request.user.is_student:
			return False
		return True


