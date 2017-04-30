from django.contrib.auth.models import AbstractUser
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
	# Avatar is done in the django-avatar package. (user.avatar).

	@property
	def person(self):
		"""
		Get the Person class from the authenticated model. 
		"""
		if hasattr(self, 'person_counselor'):
			return self.person_counselor
		elif hasattr(self, 'person_teacher'):
			return self.person_teacher
		elif hasattr(self, 'person_student'):
			return self.person_student
		return None
