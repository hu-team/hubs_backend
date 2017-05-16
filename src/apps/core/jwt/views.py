from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView

from .serializers import (
	RefreshJSONWebTokenSerializer,
)

jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class VerifyJSONWebToken(JSONWebTokenAPIView):
	"""
	API View that checks the veracity of a token, returning the token if it
	is valid.
	"""
	serializer_class = VerifyJSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenAPIView):
	"""
	API View that returns a refreshed token (with new expiration) based on
	existing token

	If 'orig_iat' field (original issued-at-time) is found, will first check
	if it's within expiration window, then copy it to the new token
	"""
	serializer_class = RefreshJSONWebTokenSerializer


refresh_jwt_token = RefreshJSONWebToken.as_view()
verify_jwt_token = VerifyJSONWebToken.as_view()
