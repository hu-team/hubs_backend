from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token

from apps.core.jwt.views import refresh_jwt_token, verify_jwt_token

router = DefaultRouter()

schema_view = get_schema_view(title='Hubs API')

urlpatterns = [
	url(r'auth/obtain', obtain_jwt_token),
	url(r'auth/refresh', refresh_jwt_token),
	url(r'auth/verify', verify_jwt_token),
	url(r'', include(router.urls)),
	url(r'^$', schema_view),
]
