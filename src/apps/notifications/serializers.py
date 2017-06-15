from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	title = serializers.CharField(read_only=True)
	message = serializers.CharField(read_only=True)
	object_type = serializers.CharField(read_only=True)
	object_key = serializers.CharField(read_only=True)
	object_data = serializers.JSONField(read_only=True)
	created_at = serializers.DateTimeField(read_only=True)
	is_read = serializers.BooleanField(required=True)

	class Meta:
		model = Notification
		fields = (
			'user', 'title', 'message', 'object_type', 'object_key', 'object_data',
			'is_read', 'created_at'
		)
