from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.absence import views

router = DefaultRouter()

urlpatterns = [

	url(r'', include(router.urls)),
]
