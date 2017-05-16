"""
Django settings for hubs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP_DIR = os.path.join(BASE_DIR, 'tmp')
CACHE_DIR = os.path.join(TMP_DIR, 'cache')
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')

DEBUG = bool(int(os.getenv('DJANGO_IS_DEBUG', True)))

from config.settings import local
try:
	os.makedirs(TMP_DIR)
	os.makedirs(CACHE_DIR)
except Exception:
	pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = local.SECRET_KEY

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'material',
	'material.admin',
	'django.contrib.admin',

	'rest_framework',
	'django_extensions',
	'avatar',

	'apps.core.apps.CoreConfig',
	'apps.school.apps.SchoolConfig',
	'apps.absence.apps.AbsenceConfig',
]
if DEBUG:
	INSTALLED_APPS += [
		'debug_toolbar',
	]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
	MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates')
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'config.wsgi.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = local.DATABASES

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

AUTH_USER_MODEL = 'core.User'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "d b Y H:i:s"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

CORS_ORIGIN_ALLOW_ALL = True

# Cache backend
if hasattr(local, 'CACHES'):
	CACHES = local.CACHES
else:
	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
			'LOCATION': CACHE_DIR,
		}
	}

# API, Rest framework.
JWT_AUTH = {
	'JWT_ENCODE_HANDLER': 'apps.core.jwt.utils.jwt_encode_handler',
	'JWT_DECODE_HANDLER': 'apps.core.jwt.utils.jwt_decode_handler',
	'JWT_PAYLOAD_HANDLER': 'apps.core.jwt.utils.jwt_payload_handler',
	'JWT_PAYLOAD_GET_USER_ID_HANDLER': 'apps.core.jwt.utils.jwt_get_user_id_from_payload_handler',
	'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'apps.core.jwt.utils.jwt_get_username_from_payload_handler',
	'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.core.jwt.utils.jwt_response_payload_handler',

	'JWT_SECRET_KEY': SECRET_KEY,
	'JWT_PUBLIC_KEY': None,
	'JWT_PRIVATE_KEY': None,
	'JWT_ALGORITHM': 'HS256',
	'JWT_VERIFY': True,
	'JWT_VERIFY_EXPIRATION': True,
	'JWT_LEEWAY': 0,
	'JWT_EXPIRATION_DELTA': datetime.timedelta(minutes=60),
	'JWT_AUDIENCE': None,
	'JWT_ISSUER': None,

	'JWT_ALLOW_REFRESH': True,
	'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=365),

	'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

REST_FRAMEWORK = {
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_RENDERER_CLASSES': (
		'rest_framework.renderers.JSONRenderer',
		'rest_framework.renderers.BrowsableAPIRenderer',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'apps.core.jwt.authentication.JWTTokenAuthentication',
		'rest_framework.authentication.TokenAuthentication',
		'apps.core.jwt.authentication.CsrfExemptSessionAuthentication',
	)
}
