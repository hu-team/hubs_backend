from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db import models
from django.db.models import Q
from django.utils.timezone import now

from apps.core.models import BaseModel, User, SimpleModel
from apps.school.utils import years_ago
from apps.school.validations import validate_school_year


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
	"""
	The counselor of the student.
	"""

	graduated = models.BooleanField(default=False)
	"""
	Wether gruadated or not.
	"""

	def get_num_years(self, end=None):
		if end is None:
			end = now()
		return int((end - self.joined_at).days / 365.25)

	@property
	def last_index_point(self):
		return self.progress_indexes.filter(complete=True).order_by('-school_year', 'period').first()


class StudentProgressIndexPoint(SimpleModel):
	PERIOD_A = 'A'
	PERIOD_B = 'B'
	PERIOD_C = 'C'
	PERIOD_D = 'D'
	PERIOD_E = 'E'
	PERIOD_CHOICES = (
		(PERIOD_A, 'A'),
		(PERIOD_B, 'B'),
		(PERIOD_C, 'C'),
		(PERIOD_D, 'D'),
		(PERIOD_E, 'E'),
	)

	TRIGGER_REASON_PRESENCE = 'presence'
	TRIGGER_REASON_GRADE = 'grade'
	TRIGGER_REASON_MIXED = 'mixed'
	TRIGGER_REASON_OTHER = 'other'
	TRIGGER_REASON_CHOICES = (
		(TRIGGER_REASON_PRESENCE, 'Presence'),
		(TRIGGER_REASON_GRADE, 'Grade'),
		(TRIGGER_REASON_MIXED, 'Mixed (Presence and grade)'),
		(TRIGGER_REASON_OTHER, 'Other'),
	)

	student = models.ForeignKey(Student, related_name='progress_indexes', db_index=True)
	period = models.CharField(db_index=True, max_length=10, choices=PERIOD_CHOICES)

	school_year = models.CharField(
		null=False,
		validators=[validate_school_year],
		max_length=9,
		help_text='School year in 2016-2017 format.',
		default='',
	)
	"""
	Year of given course.
	"""

	complete = models.BooleanField(default=False)
	"""
	Was the month complete and did we had enough data to calculate the index?
	"""

	index = models.FloatField(null=True, default=None)
	"""
	The outcome of the calculation
	"""

	triggered = models.BooleanField(default=False)
	"""
	Did we trigger the caution signal for the counselor with this month?
	"""

	triggered_reason = models.CharField(null=True, default=None, choices=TRIGGER_REASON_CHOICES, max_length=50)
	"""
	The reason of the triggered event.
	"""

	class Meta:
		unique_together = ('student', 'period', 'school_year')

	def __str__(self):
		return 'IndexPoint ({} - {}): {}, index={}, trigger={}'.format(
			self.period, self.school_year, self.student, self.index, self.triggered
		)


class Teacher(Person):
	is_counselor = models.BooleanField(default=False)
	pass


class Counselor(Teacher):
	"""
	DONT USE THIS MODEL!
	Deprecated
	"""

	class Meta:
		managed = False
		abstract = True


class Course(BaseModel):
	PERIOD_A = 'A'
	PERIOD_B = 'B'
	PERIOD_C = 'C'
	PERIOD_D = 'D'
	PERIOD_E = 'E'
	PERIOD_CHOICES = (
		(PERIOD_A, 'A'),
		(PERIOD_B, 'B'),
		(PERIOD_C, 'C'),
		(PERIOD_D, 'D'),
		(PERIOD_E, 'E'),
	)

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

	period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default=None, null=True)
	"""
	Period of given course in the year.
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

	def prefill(self):
		for student in self.group.students.all():
			absence_report_model = apps.get_model('absence', 'AbsenceReport')
			report = absence_report_model.objects.filter(
				Q(student=student) & Q(report_from__lte=self.start) & Q(
					Q(report_until__isnull=True) | Q(report_until__gte=self.start)
				)
			).first()

			Presence.objects.get_or_create(
				lesson=self,
				student=student,
				teacher=None,
				defaults=dict(
					absence_report=report,
					present=False
				)
			)


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
	"""
	Lesson
	"""

	student = models.ForeignKey(
		Student,
		db_index=True
	)
	"""
	Student
	"""

	teacher = models.ForeignKey(
		Teacher,
		null=True,
		default=None,
		db_index=True,
		blank=True
	)
	"""
	What teacher set the presence
	"""

	present = models.BooleanField(
		null=False,
		help_text='Is the student present.'
	)

	absence_report = models.ForeignKey('absence.AbsenceReport', null=True, default=None, blank=True)
	"""
	Optional report to a report that is valid at the time of creation.
	"""

	objects = PresenceManager()

	class Meta:
		unique_together = ('lesson', 'student')
