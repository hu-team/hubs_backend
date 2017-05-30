from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class BaseModel(models.Model):

	created_at = models.DateTimeField(auto_now_add=True)
	"""
	Date that the model instance was created.
	"""

	updated_at = models.DateTimeField(auto_now=True)
	"""
	Date that the model was last saved.
	"""

	class Meta:
		abstract = True


class User(AbstractUser):
	# Override to increase max_length.
	first_name = models.CharField(_('first name'), max_length=150, blank=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True)

	# Avatar is done in the django-avatar package. (user.avatar).

	@property
	def person(self):
		"""
		Get the Person class from the authenticated model.
		"""
		if hasattr(self, 'person_teacher'):
			return self.person_teacher
		elif hasattr(self, 'person_student'):
			return self.person_student
		return None

	@property
	def is_counselor(self):
		return hasattr(self, 'person_teacher') and self.person_teacher.is_counselor

	@property
	def is_teacher(self):
		return hasattr(self, 'person_teacher')

	@property
	def is_student(self):
		return hasattr(self, 'person_student')
