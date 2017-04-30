from django.db import models

from apps.core.models import BaseModel, User
from apps.school.utils import validate_school_year


class Person(BaseModel):
	user = models.OneToOneField(User, related_name='person_%(class)s')
	"""
	Link to auth user model. Will shadow all personal details like name and email from and to there.
	"""

	class Meta:
		abstract = True

	@property
	def full_name(self):
		return self.user.get_full_name() or self.user.username

	def __str__(self):
		return self.user.get_full_name() or self.user.username


class Student(Person):
	joined_at = models.DateTimeField()
	"""
	Date that the student joined the school.
	"""


class Teacher(Person):
	pass


class Counselor(Teacher):
	pass


class Course(BaseModel):
	code = models.CharField(
		null=False,
		max_length=100,
	)
	"""
	Course code, given by the school
	"""

	school_year = models.CharField(
		null=False,
		validators=[validate_school_year],
		max_length=9,
		help_text='School year in 2016-2017 format.'
	)
	"""
	Year of given course.
	"""

	name = models.CharField(
		null=True,
		blank=True,
		default=None,
		max_length=250
	)
	"""
	The optional name of the course.
	"""

	teachers = models.ManyToManyField(
		Teacher
	)
	"""
	Teachers giving this course to the students.
	"""

	class Meta:
		unique_together = ('code', 'school_year')

	def __str__(self):
		return '{} ({})'.format(self.code, self.school_year)


class Group(BaseModel):
	code = models.CharField(
		max_length=50,
		help_text='Student class code.',
	)
	"""
	The group (class) code (V3A for example).
	"""

	school_year = models.CharField(
		validators=[validate_school_year],
		max_length=9,
		help_text='School year in 2016-2017 format.'
	)
	"""
	Year of class group.
	"""

	students = models.ManyToManyField(
		Student,
		related_name='groups'
	)
	"""
	Students that are inside of this group.
	"""

	class Meta:
		unique_together = ('code', 'school_year')


class Lesson(BaseModel):
	course = models.ForeignKey(Course, related_name='lessons')
	"""
	The course of the current lesson.
	"""

	ignore_absence = models.BooleanField(
		default=False,
		help_text=
		'Check this to ignore the absence reports, and lower the weight of the absence of the students. '
		'this is useful when this lesson is an extra lesson and only some students will follow it.'
	)
	"""
	Ignore absence (lower weight in formula).
	"""

	teacher = models.ForeignKey(
		Teacher,
		help_text='Select the teacher that is giving this lesson.'
	)
	"""
	Teacher that is giving this lesson.
	"""

	group = models.ForeignKey(
		Group,
		help_text='The group that got this lesson.'
	)
	"""
	Group of students (class).
	"""

	start = models.DateTimeField(
		help_text='Start date and time of the lesson'
	)
	"""
	Start date+time
	"""

	end = models.DateTimeField(
		help_text='End date and time of the lesson'
	)
	"""
	End date+time
	"""
