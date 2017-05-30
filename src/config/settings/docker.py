import os

SECRET_KEY = 'chanafhsdfjasdfhklgeme'

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'hubs',
		'USER': 'root',
		'PASSWORD': 'hubs',
		'HOST': 'mysql',
		'PORT': 3306,
	}
}

if bool(int(os.getenv('DJANGO_IS_DEBUG', 0))):
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
		}
	}
else:
	CACHES = {
		'default': {
			'BACKEND': 'django_redis.cache.RedisCache',
			'LOCATION': 'redis://redis:6379/0',
			'OPTIONS': {
				'CLIENT_CLASS': 'django_redis.client.DefaultClient',
			}
		}
	}

	SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
	SESSION_CACHE_ALIAS = 'default'


def show_toolbar(request):
	if request.is_ajax():
		return False
	return True

DEBUG_TOOLBAR_CONFIG = {
	'SHOW_TOOLBAR_CALLBACK': 'config.settings.docker.show_toolbar',
}
