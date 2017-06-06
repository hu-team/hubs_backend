from celery.task import task


@task
def check_debug(**kwargs):
	print('Test')
