from datetime import timedelta

import os
import pymysql
from celery.schedules import crontab

pymysql.install_as_MySQLdb()

DEBUG = bool(int(os.getenv('DJANGO_IS_DEBUG', True)))

if DEBUG:
	from .dev import *
else:
	from .live import *

if bool(os.getenv('DJANGO_DOCKER', False)):
	from .docker import *

DEBUG = bool(int(os.getenv('DJANGO_IS_DEBUG', True)))

#

CELERYBEAT_SCHEDULE = {
	'debug-check': {
		'task': 'apps.core.tasks.check_debug',
		'schedule': timedelta(minutes=5),
	},
	'daily-index-calculation': {
		'task': 'apps.school.tasks.daily_process_student_progress_index',
		'schedule': crontab(hour='1', minute='0'),
	},
}


from celeryApp import app as celery_app
