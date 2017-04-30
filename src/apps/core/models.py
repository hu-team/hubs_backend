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
	avatar = models.ImageField(blank=True, upload_to='avatars/', default='')
	"""
	Optional avatar for the specific user.
	"""
