from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from . import views


router = DefaultRouter(trailing_slash=False)
router.register(r'lessons', views.LessonViewSet)
router.register(r'groups', views.GroupViewSet, base_name='groups')
router.register(r'presences', views.PresenceViewSet, base_name='presences-detail')
router.register(r'courses', views.CourseViewSet, base_name='courses')
router.register(r'results', views.ResultViewSet, base_name='results')

schema_view = get_schema_view(title='Hubs API')

urlpatterns = [
	url(r'', include(router.urls)),
	url(r'^$', schema_view),
]
