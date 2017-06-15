from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.notifications import views

router = DefaultRouter()
router.register(r'notifications', views.NotificationViewSet, base_name='notifications')

urlpatterns = [
	url(r'', include(router.urls)),
]
