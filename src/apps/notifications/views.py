from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.core.permissions import StudentNotAllowed
from apps.notifications.models import Notification
from apps.notifications import serializers


class NotificationViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet
):
	permission_classes = [StudentNotAllowed]
	model = Notification
	queryset = Notification.objects.all().order_by('-created_at')
	serializer_class = serializers.NotificationSerializer

	def get_queryset(self):
		return super().get_queryset().filter(user=self.request.user)


class NotificationMiniViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet
							):
	permission_classes = [StudentNotAllowed]
	model = Notification
	queryset = Notification.objects.all().order_by('-created_at')
	serializer_class = serializers.NotificationMiniSerializer

	def get_queryset(self):
		return super().get_queryset().filter(user=self.request.user)
