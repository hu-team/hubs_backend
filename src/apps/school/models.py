from django.db import models

from apps.core.models import BaseModel, User
from apps.school.utils import validate_school_year


class PersonManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().select_related('user')


class Person(BaseModel):
	user = models.OneToOneField(User, related_name='person_%(class)s')
	"""
	Link to auth user model. Will shadow all personal details like name and email from and to there.
	"""

	objects = PersonManager()

	class Meta:
		abstract = True

	@property
	def full_name(self):
		return self.user.get_full_name() or self.user.username

	def __str__(self):
		return self.user.get_full_name() or self.user.username


class Student(Person):
	student_number = models.CharField(max_length=128, null=True, default=None, unique=True)
	"""
	Student number.
	"""

	joined_at = models.DateTimeField()
	"""
	Date that the student joined the school.
	"""

	counselor = models.ForeignKey('Teacher', related_name='students', null=True, default=None)


class Teacher(Person):
	is_counselor = models.BooleanField(default=False)
	pass


class Counselor(Teacher):
	"""
	DONT USE THIS MODEL!
	"""

	class Meta:
		managed = False
		abstract = True


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

	ec_points = models.PositiveIntegerField(
		null=False,
		help_text='EC Points that the student can get.'
	)
	"""
	The maximum EC points the student can get.
	"""

	number_essays = models.PositiveIntegerField(
		null=False,
		help_text='Number of essays and thus results the student can get on this course.'
	)
	"""
	Number of essays the student gets in this course.
	"""

	number_resits = models.PositiveIntegerField(
		null=False,
		default=1,
		help_text='Number of resits possible.'
	)
	"""
	Number of resits possible.
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

	def __str__(self):
		return self.code


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

	def __str__(self):
		return '{}: from {} until {}'.format(str(self.course), self.start, self.end)


class Result(BaseModel):
	LADDER_NT = 0
	LADDER_FAIL = 1
	LADDER_PASS = 2
	LADDER_CHOICES = (
		(LADDER_NT, 'Not present'),
		(LADDER_FAIL, 'Failed'),
		(LADDER_PASS, 'Passed'),
	)

	course = models.ForeignKey(
		Course
	)
	"""
	Course of the result entry.
	"""

	student = models.ForeignKey(
		Student,
		related_name='results',
		db_index=True
	)
	"""
	Student of the result entry.
	"""

	ec_points = models.PositiveIntegerField(
		null=True,
		help_text='The EC Points the student got with this result.'
	)
	"""
	The EC Points the student got with this result.
	"""

	number_grade = models.PositiveIntegerField(
		null=True,
		help_text='The grade from 0 to 10 where 0 is not present and 10 is fully passed.'
	)
	"""
	Number grade.
	"""

	ladder_grade = models.DecimalField(
		choices=LADDER_CHOICES,
		null=True,
		max_digits=2,
		decimal_places=1,
		help_text='The grade in ladder format.'
	)
	"""
	Ladder grade.
	"""

	resit = models.BooleanField(
		default=False,
		help_text='Is this result from a resit essay.'
	)
	"""
	Resit attribute.
	"""


class PresenceManager(models.Manager):

	def get_queryset(self):
		return super().get_queryset().select_related('lesson', 'student')


class Presence(BaseModel):
	lesson = models.ForeignKey(
		Lesson,
		db_index=True
	)

	student = models.ForeignKey(
		Student,
		db_index=True
	)

	present = models.BooleanField(
		null=False,
		help_text='Is the student present.'
	)

	absence_report = models.ForeignKey('absence.AbsenceReport', null=True, default=None)
	"""
	Optional report to a report that is valid at the time of creation.
	"""

	objects = PresenceManager()

	class Meta:
		unique_together = ('lesson', 'student')
