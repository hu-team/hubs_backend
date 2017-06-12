from celery.task import task


@task
def process_student_progress_index(**kwargs):
	print('Test')
