from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from . import views


router = DefaultRouter()
router.register(r'lessons', views.LessonViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'presences', views.PresenceViewSet)

schema_view = get_schema_view(title='Hubs API')

urlpatterns = [
	url(r'', include(router.urls)),
	url(r'^$', schema_view),
]
