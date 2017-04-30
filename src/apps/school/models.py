from django.db import models

from apps.core.models import BaseModel, User


class Person(BaseModel):
	user = models.OneToOneField(User, related_name='person_%(class)s')
	"""
	Link to auth user model. Will shadow all personal details like name and email from and to there.
	"""

	class Meta:
		abstract = True


class Student(Person):
	joined_at = models.DateTimeField()
	"""
	Date that the student joined the school.
	"""


class Teacher(Person):
	pass


class Counselor(Teacher):
	pass
