import uuid
import warnings
from pprint import pprint

import jwt

from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework_jwt.compat import get_username_field, get_username
from rest_framework_jwt.settings import api_settings

from apps.core.serializers import UserApiSerializer
from apps.school.models import Teacher, Student


def jwt_payload_handler(payload):
	if isinstance(payload, dict):
		user = payload['user']
	else:
		user = payload

	username_field = get_username_field()
	username = get_username(user)

	user_type = 'unknown'
	if user.person and isinstance(user.person, Teacher):
		if user.person.is_counselor:
			user_type = 'counselor'
		else:
			user_type = 'teacher'
	elif user.person and isinstance(user.person, Student):
		user_type = 'student'

	payload = {
		'user_id': user.pk,
		'email': user.email,
		'username': username,
		'user_type': user_type,
		'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
	}
	if isinstance(user.pk, uuid.UUID):
		payload['user_id'] = str(user.pk)

	payload[username_field] = username

	# Include original issued at time for a brand new token,
	# to allow token refresh
	if api_settings.JWT_ALLOW_REFRESH:
		payload['orig_iat'] = timegm(
			datetime.utcnow().utctimetuple()
		)

	if api_settings.JWT_AUDIENCE is not None:
		payload['aud'] = api_settings.JWT_AUDIENCE

	if api_settings.JWT_ISSUER is not None:
		payload['iss'] = api_settings.JWT_ISSUER

	return payload


def jwt_get_user_id_from_payload_handler(payload):
	"""
	Override this function if user_id is formatted differently in payload
	"""
	warnings.warn(
		'The following will be removed in the future. '
		'Use `JWT_PAYLOAD_GET_USERNAME_HANDLER` instead.',
		DeprecationWarning
	)

	return payload.get('user_id')


def jwt_get_username_from_payload_handler(payload):
	"""
	Override this function if username is formatted differently in payload
	"""
	return payload.get('username')


def jwt_response_payload_handler(token, payload=None, request=None):
	"""
	Returns the response data for both the login and refresh views.
	Override to return a custom response such as including the
	serialized representation of the User.

	Example:

	def jwt_response_payload_handler(token, user=None, request=None):
		return {
			'token': token,
			'user': UserSerializer(user, context={'request': request}).data
		}

	"""
	if isinstance(payload, dict):
		user = payload['user']
	else:
		user = payload

	if not user or not isinstance(user, get_user_model()):
		return {
			'token': token,
			'user': None,
		}

	return {
		'token': token,
		'user': UserApiSerializer(user, context={'request': request}).data,
	}


def jwt_decode_handler(token, options=None):
	if type(options) != dict:
		options = {
			'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
		}

	return jwt.decode(
		token,
		api_settings.JWT_PUBLIC_KEY or api_settings.JWT_SECRET_KEY,
		api_settings.JWT_VERIFY,
		options=options,
		leeway=api_settings.JWT_LEEWAY,
		audience=api_settings.JWT_AUDIENCE,
		issuer=api_settings.JWT_ISSUER,
		algorithms=[api_settings.JWT_ALGORITHM]
	)


def jwt_encode_handler(payload):
	return jwt.encode(
		payload,
		api_settings.JWT_PRIVATE_KEY or api_settings.JWT_SECRET_KEY,
		api_settings.JWT_ALGORITHM
	).decode('utf-8')
