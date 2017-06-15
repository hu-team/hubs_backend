from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apps.notifications.models import Notification
from apps.notifications import serializers


class NotificationViewSet(
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	mixins.UpdateModelMixin,
	viewsets.GenericViewSet
):
	permission_classes = [IsAuthenticated]
	model = Notification
	queryset = Notification.objects.all()
	serializer_class = serializers.NotificationSerializer

	def get_queryset(self):
		return super().get_queryset().filter(user=self.request.user)
