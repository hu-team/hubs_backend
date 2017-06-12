from celery.task import task

from apps.school.models import Student


@task
def daily_process_student_progress_index(**kwargs):
	for student in Student.objects.all().prefetch_related('progress_indexes'):
		print(student)
