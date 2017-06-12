import random
import string
import typing
import datetime

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
	for n in range(int ((end_date - start_date).days)):
		yield start_date + datetime.timedelta(n)


class Command(BaseCommand):
	help = 'Insert sample data (generated / predefined) into the current database.'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_fake(self):
		return Factory.create('nl_NL')

	def get_random_str(self, num_chars):
		return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))

	def handle(self, *args, **options):
		# Create admin.
		try:
			User.objects.create_superuser('admin', 'admin@localhost', 'Welkom01', first_name='Admin')
		except:
			pass  # Ignore if duplicate.

		# Create test courses, groups and
		print('Generating courses...')
		self.create_courses(4)

	def create_courses(self, num):
		for c_idx in range(num):
			fprint('Creating courses... {} out of {}...'.format(c_idx+1, num))
			# Generate users.
			teachers = list(self.generate_teachers(4))
			slbers = list(self.generate_slbers(2))

			# Decide school year
			school_years = list(self.school_year_range(years_back=4))

			# Generate courses. Including groups and students..
			courses = list()
			groups = list()
			for years_back, (year, year_start, year_end) in enumerate(reversed(school_years)):
				period = random.choice(Course.PERIOD_CHOICES)

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
				for gpidx in range(3):
					# Generate students.
					students = list(self.generate_students(24, years_back=years_back))

					# Create group.
					group = Group.objects.create(
						code='V{}{}-{}'.format(
							4-years_back, gpidx+1, self.get_random_str(6).upper()
						),
						school_year=year,
					)
					group.students = students
					group.save()
					groups.append(group)

					result_date = year_start + datetime.timedelta(days=30)

					# Generate results.
					for student in students:
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
					for single_day in daterange(year_start, year_end):
						# Check if between the lesson months.
						if single_day.month == 7:
							continue

						# Check if not in weekend.
						if single_day.weekday() >= 5:
							continue

						# Randomly generate it, not every day.
						if not random.getrandbits(1):
							continue

						# Random start and end time.
						start_hour = random.randint(9, 12)
						start = datetime.datetime(
							year=single_day.year, month=single_day.month, day=single_day.day, hour=start_hour, minute=0,
							tzinfo=utc
						)
						end = start + datetime.timedelta(hours=2)

						lesson = Lesson.objects.create(
							course=course,
							teacher=random.choice(teachers),
							group=group,
							start=start,
							end=end,
							ignore_absence=bool(random.getrandbits(1) and random.getrandbits(1))
						)

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

	def generate_students(self, num, years_back=None):
		for i in range(0, num):
			fake = self.get_fake()
			user = self.generate_user(fake)
			if years_back is None:
				join_date = fake.date_time_between(start_date='-5y', end_date='now', tzinfo=utc)
			else:
				join_date = datetime.datetime(year=timezone.now().year - years_back, month=7, day=1, tzinfo=utc)
			yield Student.objects.create(
				user=user,
				joined_at=join_date
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

	def school_year_range(self, years_back):
		now = timezone.now()
		now += relativedelta(years=2)
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

