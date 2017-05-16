import jwt

from calendar import timegm
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class Serializer(serializers.Serializer):
	@property
	def object(self):
		return self.validated_data


class VerificationBaseSerializer(Serializer):
	"""
	Abstract serializer used for verifying and refreshing JWTs.
	"""
	token = serializers.CharField()

	def validate(self, attrs):
		msg = 'Please define a validate method.'
		raise NotImplementedError(msg)

	def _check_payload(self, token, allow_expired=False):
		# Check payload valid (based off of JSONWebTokenAuthentication,
		# may want to refactor)
		options = None if not allow_expired else {'verify_exp': False}

		try:
			payload = jwt_decode_handler(token, options=options)
		except jwt.ExpiredSignature:
			msg = _('Signature has expired.')
			raise serializers.ValidationError(msg)
		except jwt.DecodeError:
			msg = _('Error decoding signature.')
			raise serializers.ValidationError(msg)

		return payload

	def _check_user(self, payload):
		username = jwt_get_username_from_payload(payload)

		if not username and username != '':
			msg = _('Invalid payload.')
			raise serializers.ValidationError(msg)

		# Make sure user exists
		try:
			user = User.objects.get_by_natural_key(username)
		except User.DoesNotExist:
			msg = _("User doesn't exist.")
			raise serializers.ValidationError(msg)

		if username and not user.is_active:
			msg = _('User account is disabled.')
			raise serializers.ValidationError(msg)

		return user


class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
	"""
	Refresh an access token.
	"""

	def validate(self, attrs):
		token = attrs['token']

		payload = self._check_payload(token=token, allow_expired=True)
		user = self._check_user(payload=payload)

		# Get and check 'orig_iat'
		orig_iat = payload.get('orig_iat')

		if orig_iat:
			# Verify expiration
			refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

			if isinstance(refresh_limit, timedelta):
				refresh_limit = (refresh_limit.days * 24 * 3600 +
								 refresh_limit.seconds)

			expiration_timestamp = orig_iat + int(refresh_limit)
			now_timestamp = timegm(datetime.utcnow().utctimetuple())

			if now_timestamp > expiration_timestamp:
				msg = _('Refresh has expired.')
				raise serializers.ValidationError(msg)
		else:
			msg = _('orig_iat field is required.')
			raise serializers.ValidationError(msg)

		new_payload = jwt_payload_handler(dict(user=user, instance=instance))
		new_payload['orig_iat'] = orig_iat

		return {
			'token': jwt_encode_handler(new_payload),
			'user': user,
		}


class CreateJSONWebTokenSerializer(Serializer):
	"""
	Create an access token.
	"""
	pass
