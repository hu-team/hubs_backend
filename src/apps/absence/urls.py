from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.absence import views

router = DefaultRouter()
router.register(r'absencereports', views.AbsenceReportViewSet, base_name='absencereports-detail')

urlpatterns = [

	url(r'', include(router.urls)),
]
