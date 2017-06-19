import logging
from celery.task import task
from django.utils.timezone import now

from apps.notifications.models import Notification
from apps.school.models import Student, Course, StudentProgressIndexPoint, Result, Lesson
from apps.school.utils import calculate_index

TRIGGER_BELOW = 40


@task
def daily_process_student_progress_index(**kwargs):
	logger = logging.getLogger(__name__)

	queryset = Student.objects \
		.filter(graduated=False) \
		.prefetch_related('progress_indexes', 'groups')
	total_students = len(queryset)
	current_student = 0

	for student in queryset:
		current_student += 1
		logger.info('Processing student {}/{}: \'{}\'...'.format(current_student, total_students, student))

		courses = list()

		# Add all courses.
		for group in student.groups.all():
			course_ids = list(group.lesson_set.values('course').distinct())
			for c in [Course.objects.get(pk=i['course']) for i in course_ids]:
				courses.append((group, c))

		# Loop over course + periods.
		for group, course in courses:
			# Get the index or create it if it doesn't exist.
			index, created = StudentProgressIndexPoint.objects.get_or_create(
				student=student, period=course.period, school_year=course.school_year,
			)

			# Get all results for this course and student.
			results = Result.objects.filter(course=course, student=student)

			# Check if we have all results complete.
			course_results_complete = bool(len(results) >= course.number_essays)

			# Check if the period is over (check the last lesson).
			last_lesson = group.lesson_set.filter(course=course).order_by('-end').first()
			course_lessons_done = last_lesson and last_lesson.end <= now()

			index.complete = course_results_complete and course_lessons_done
			index.triggered_reason = None
			if not course_results_complete:
				index.index = None
				index.triggered = False

			else:
				# Calculate index
				index.index, situation = calculate_index(student, course, group, results)

				# Save the old trigger in a var
				was_trigged = index.triggered

				# Set trigger.
				index.triggered = bool(index.index is not None and index.index < TRIGGER_BELOW)

				# Create a notification
				if not was_trigged and index.triggered:
					Notification.objects.create(
						user=student.counselor.user,
						title='Student Trigger Alert',
						message="Er is een trigger afgegaan voor {}.".format(student.full_name),
						object_type='trigger-notificatie',
						object_key=student.id)

				# Set trigger reason.
				if index.triggered and situation:
					if situation.a >= 10:
						index.triggered_reason = StudentProgressIndexPoint.TRIGGER_REASON_PRESENCE
					if situation.avg_grade <= 6.0:
						if index.triggered_reason:
							index.triggered_reason = StudentProgressIndexPoint.TRIGGER_REASON_MIXED
						else:
							index.triggered_reason = StudentProgressIndexPoint.TRIGGER_REASON_GRADE

			# Save model.
			index.save()
