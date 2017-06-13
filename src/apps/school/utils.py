import logging

import datetime
from dateutil import relativedelta
from django.utils.timezone import now

from apps.school import algorithm


def calculate_index(student, course, group, results):
	"""
	Calculate the index. Will refer to the util method.

	:param student: Student model instance.
	:param course: Course model instance.
	:param group: Group model instance.
	:param results: Results model instance.
	:return: Index in float or None.
	"""
	logger = logging.getLogger(__name__)
	from apps.school.models import Lesson, Presence

	# First of all, we need to get the students lessons presence of the period.
	lessons = Lesson.objects.filter(course=course, group=group)

	####################################################################################################################
	# Calculate the presence part of the formula.
	total_lessons = 0
	total_hours = 0.
	total_lessons_present = 0
	total_hours_present = 0.

	last_lesson_date = None
	for lesson in lessons:
		lesson_time = lesson.end - lesson.start
		lesson_hours = lesson_time.total_seconds() / 3600.0

		if not last_lesson_date or last_lesson_date < lesson.end:
			last_lesson_date = lesson.end

		if lesson.start >= now():
			continue

		try:
			presence = Presence.objects.get(lesson=lesson, student=student)
		except Presence.DoesNotExist:
			logger.info('Has no presence for student=\'{}\' and lesson=\'{}\''.format(student, lesson))
			if lesson.start <= (now() - datetime.timedelta(days=7)):
				# Force the prefill so it has data.
				logger.info('Prefilling lesson in the cron task!')
				lesson.prefill()

			# Get it again.
			try:
				presence = Presence.objects.get(lesson=lesson, student=student)
			except Presence.DoesNotExist:
				continue

		if presence.present or lesson.ignore_absence:
			total_lessons_present += 1
			total_hours_present += lesson_hours
		total_lessons += 1
		total_hours += lesson_hours

	# This happens when the lessons are in the future.
	if total_hours <= 0:
		return None, None

	####################################################################################################################
	# Get and uniform all grades of the student.
	grades = list()
	for result in results:
		if result.number_grade is not None:
			grades.append(result.number_grade)
		elif result.ladder_grade is not None:
			if result.ladder_grade == result.LADDER_PASS:
				grades.append(6)
			else:
				grades.append(0)
		else:
			grades.append(0)

	logger.debug('Student \'{}\' in period {}: grades={}, hours_present={}/{}'.format(
		student, course.period, grades, total_hours_present, total_hours
	))

	####################################################################################################################
	# Calculate!
	student_school_years = student.get_num_years()

	situation = algorithm.Situation(
		hours_present=total_hours_present, total_hours=total_hours,
		year_of_study=student_school_years, grades=grades
	)

	return situation.calculate(), situation


def years_ago(years, from_date=None):
	if from_date is None:
		from_date = now()
	try:
		return from_date.replace(year=from_date.year - years)
	except ValueError:
		# Must be 2/29!
		assert from_date.month == 2 and from_date.day == 29  # can be removed
		return from_date.replace(month=2, day=28, year=from_date.year-years)

