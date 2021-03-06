import random
import string
import typing
import datetime

import sys
from dateutil.relativedelta import relativedelta
from django.utils.timezone import utc
from faker import Factory

from django.core.management import BaseCommand
from django.utils import timezone

from apps.core.models import User
from apps.school.models import Student, Teacher, Group, Lesson, Course, Result


def fprint(msg):
	print('{}\r'.format(msg))


def daterange(start_date, end_date) -> typing.Generator[datetime.datetime, datetime.datetime, None]:
	"""
	:param start_date:
	:param end_date:
	:return:
	:rtype: datetime.datetime
	"""
	for n in range(int((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)


def period_dates(year, period):
	if period == 'A':
		return datetime.datetime(year=year, month=9, day=1), datetime.datetime(year=year, month=11, day=1)
	elif period == 'B':
		return datetime.datetime(year=year, month=11, day=2), datetime.datetime(year=year+1, month=1, day=30)
	elif period == 'C':
		return datetime.datetime(year=year+1, month=2, day=1), datetime.datetime(year=year+1, month=4, day=1)
	elif period == 'D':
		return datetime.datetime(year=year+1, month=4, day=2), datetime.datetime(year=year+1, month=6, day=19)
	elif period == 'E':
		return datetime.datetime(year=year+1, month=6, day=20), datetime.datetime(year=year+1, month=8, day=28)


def period_range(year, period):
	start, end = period_dates(year, period)
	return daterange(start, end)


class Command(BaseCommand):
	help = 'Insert sample data (generated / predefined) into the current database.'

	def __init__(self, *args, **kwargs):
		self.student_id = 1000001
		self.period = 'A'
		self.small = False

		super().__init__(*args, **kwargs)

	def add_arguments(self, parser):
		parser.add_argument('--small', action='store_true')

	def get_fake(self):
		return Factory.create('nl_NL')

	def get_random_str(self, num_chars):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))

	def handle(self, *args, **options):
		self.small = bool(options['small'])

		# Create admin.
		try:
			User.objects.create_superuser('admin', 'admin@localhost', 'Welkom01', first_name='Admin')
		except:
			pass  # Ignore if duplicate.

		# Create test courses, groups and
		if self.small:
			self.create_courses(4)
		else:
			self.create_courses(4*2)

	def create_courses(self, num):
		# Decide school years
		school_years = list(self.school_year_range(years_back=4))

		students_per_group = 14
		if self.small:
			students_per_group = 6

		# Generate students.
		fprint('Creating persons...')
		slbers = list(self.generate_slbers(2*num))
		teachers = list(self.generate_teachers(4*num))
		students = list(self.generate_students(((students_per_group - 2)*2), years_back=None, slbers=slbers))

		static_student, static_teacher, static_slber = self.generate_static()
		students.append(static_student)
		teachers.append(static_teacher)
		slbers.append(static_slber)

		# Generate predefined groups.
		fprint('Creating groups...')
		predef_groups = list()
		for group_number in range(int(len(students) / students_per_group)):
			# Get the students for this group.
			group_students = list()
			for _ in range(students_per_group):
				random_student = random.choice(students)
				if random_student in group_students:
					continue
				group_students.append(random_student)

			# Generate each year.
			group_set = list()

			for years_back, (year, year_start, year_end) in enumerate(reversed(school_years)):
				for period, _ in Course.PERIOD_CHOICES:
					group = Group.objects.create(
						code='VC{}-{}-{}'.format(
							4-years_back, group_number, period
						),
						school_year=year,
					)
					group.students = group_students
					group.save()
					group_set.append(group)

			predef_groups.append(group_set)

		courses = list()
		groups = list()

		for c_idx in range(num):
			print(' ')
			fprint('Creating course... {} out of {}...'.format(c_idx+1, num))

			period = self.next_period()

			for years_back, (year, year_start, year_end) in enumerate(reversed(school_years)):
				course = Course.objects.create(
					code='{}-{}'.format(self.get_random_str(3).upper(), self.get_random_str(6).upper()),
					school_year=year,
					name='Course \'{}\''.format(self.get_fake().job()),
					ec_points=5, number_essays=2, number_resits=1,
					period=period,
				)
				course.teachers = teachers+slbers
				course.save()
				courses.append(course)

				# Generate groups
				for group_list in predef_groups:
					for group in group_list:
						groups.append(group)

						# Calculate the last day of the period as a result date.
						result_date = period_dates(year_start.year, period)[1]

						# Generate results.
						for student in group.students.all():
							for i in range(0, 2):
								is_ladder = bool(random.getrandbits(1))
								ladder_grade = None
								number_grade = None
								ec_points = 0

								passed = bool(random.getrandbits(1)) or bool(random.getrandbits(1))
								not_there = bool(random.getrandbits(1)) and bool(random.getrandbits(1)) and bool(random.getrandbits(1))
								if is_ladder:
									if not_there:
										ladder_grade = Result.LADDER_NT
									elif passed:
										ladder_grade = Result.LADDER_PASS
										ec_points = 5
									else:
										ladder_grade = Result.LADDER_FAIL
								else:
									if not_there:
										number_grade = 0.0
									elif passed:
										number_grade = round(random.uniform(5.5, 10.0), 1)
									else:
										number_grade = round(random.uniform(1.0, 5.4), 1)
									if number_grade >= 5.5:
										ec_points = 5

								Result.objects.create(
									course=course, student=student, ec_points=ec_points,
									ladder_grade=ladder_grade, number_grade=number_grade,
									created_at=result_date,
								)

								if ec_points == 0:
									passed = bool(random.getrandbits(1)) or bool(random.getrandbits(1))
									Result.objects.create(
										course=course, student=student, ec_points=5 if passed else 0,
										ladder_grade=Result.LADDER_PASS if passed else Result.LADDER_FAIL, number_grade=None,
										resit=True,
										created_at=result_date + datetime.timedelta(days=4)
									)

						# Generate lessons (for each days (some randomized stuff)).
						lessons = list()
						for single_day in period_range(year_start.year, period):
							# Check if between the lesson months.
							if single_day.month == 7:
								continue

							# Check if not in weekend.
							if single_day.weekday() >= 5:
								continue

							# Randomly generate it, not every day. 70% chance (or 85 when small) of skipping and no lesson on that day.
							percentage = 70
							if self.small:
								percentage = 85
							if not bool(random.randrange(100) < percentage):
								continue

							# Random start and end time.
							start_hour = random.randint(9, 12)
							start = datetime.datetime(
								year=single_day.year, month=single_day.month, day=single_day.day, hour=start_hour, minute=0,
								tzinfo=utc
							)
							end = start + datetime.timedelta(hours=2)

							lessons.append(Lesson(
								course=course,
								teacher=random.choice(teachers),
								group=group,
								start=start,
								end=end,
								ignore_absence=bool(random.getrandbits(1) and random.getrandbits(1))
							))

						# Bulk create.
						print('.', end='', sep='', flush=True)
						Lesson.objects.bulk_create(lessons)

		print(' ')
		fprint('Prefilling lessons...')
		lessons = Lesson.objects.all()
		total_lessons = len(lessons)
		for idx, lesson in enumerate(lessons):
			print('.', end='', sep='', flush=True)
			if idx % 100 == 0:
				print(' {}% '.format(
					int(idx / total_lessons * 100)
				), end='', sep='', flush=True)

			# Generate presence for lessons at least one year ago.
			if lesson.start <= (timezone.now() - relativedelta(years=1)):
				lesson.prefill()

				# Randomize the presence status.
				for presence in lesson.presence_set.all():
					presence.present = bool(random.randrange(100) < 90)  # 90 percentage chance of present.
					presence.save()

	def next_period(self):
		if self.period == 'A':
			self.period = 'B'
		elif self.period == 'B':
			self.period = 'C'
		elif self.period == 'C':
			self.period = 'D'
		elif self.period == 'D':
			self.period = 'E'
		elif self.period == 'E':
			self.period = 'A'
		return self.period

	def generate_teachers(self, num):
		for i in range(0, num):
			fake = self.get_fake()
			user = self.generate_user(fake)
			yield Teacher.objects.create(
				user=user
			)

	def generate_slbers(self, num):
		for i in range(0, num):
			fake = self.get_fake()
			user = self.generate_user(fake)
			yield Teacher.objects.create(
				user=user,
				is_counselor=True,
			)

	def generate_students(self, num, years_back=None, slbers=None):
		for i in range(0, num):
			fake = self.get_fake()
			user = self.generate_user(fake)

			student_number = self.student_id
			self.student_id += 1

			counselor = None
			if slbers:
				counselor = random.choice(slbers)

			if years_back is None:
				join_date = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=utc)
			else:
				join_date = datetime.datetime(year=timezone.now().year - years_back, month=7, day=1, tzinfo=utc)
			yield Student.objects.create(
				user=user,
				joined_at=join_date,
				counselor=counselor,
				student_number=student_number,
			)

	def generate_courses(self, num):
		for i in range(0, num):
			fake = self.get_fake()
			school_begin_year = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=None).year
			school_end_year = school_begin_year + 1
			yield Course.objects.create(
				code='{}-{}'.format(self.get_random_str(3).upper(), self.get_random_str(6).upper()),
				school_year='{}-{}'.format(school_begin_year, school_end_year)
			)

	def generate_user(self, fake=None):
		if not fake:
			fake = self.get_fake()
		user = None
		while user is None:
			try:
				user = User.objects.create_user(
					fake.user_name(), fake.email(), 'Welkom01', first_name=fake.first_name()[:], last_name=fake.last_name()
				)
			except:
				pass
		return user

	def generate_static(self):
		counselor = Teacher.objects.create(
			user=User.objects.create_user(
				username='static_counselor', email='static_counselor@gmail.com', first_name='Arjan', last_name='de Man',
				password='Welkom01'
			),
			is_counselor=True
		)
		teacher = Teacher.objects.create(
			user=User.objects.create_user(
				username='static_teacher', email='static_teacher@gmail.com', first_name='Henk', last_name='de Man',
				password='Welkom01'
			),
			is_counselor=False
		)
		student = Student.objects.create(
			user=User.objects.create_user(
				username='static_student', email='static_student@gmail.com', first_name='Jan', last_name='de Man',
				password='Welkom01'
			),
			counselor=counselor,
			joined_at=datetime.datetime(year=timezone.now().year - 4, month=7, day=1, tzinfo=utc),
			student_number=1000000,
		)
		return student, teacher, counselor

	def school_year_range(self, years_back):
		now = timezone.now()
		# now += relativedelta(years=1)
		if now.month > 6:
			this_year = (
				datetime.datetime(year=now.year, month=8, day=1, tzinfo=utc),
				datetime.datetime(year=now.year-1, month=6, day=30, tzinfo=utc)
			)
		else:
			this_year = (
				datetime.datetime(year=now.year-1, month=8, day=1, tzinfo=utc),
				datetime.datetime(year=now.year, month=6, day=30, tzinfo=utc)
			)
		for back in reversed(range(years_back)):
			back_start = this_year[0].replace(year=this_year[0].year - back)
			back_end = this_year[1].replace(year=this_year[1].year - back)
			yield (
				'{}-{}'.format(back_start.year, back_end.year),
				back_start, back_end
			)

	class Random:
		@staticmethod
		def school_year():
			school_begin_year = Factory.create('nl_NL').date_time_between(start_date='-5y', end_date='now', tzinfo=None).year
			school_end_year = school_begin_year + 1
			return '{}-{}'.format(school_begin_year, school_end_year)

