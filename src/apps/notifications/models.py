from django.db import models
from rest_framework.fields import JSONField

from apps.core.models import BaseModel, User


class Notification(BaseModel):
	user = models.ForeignKey(User, related_name='notifications', db_index=True)
	"""
	The receiving user of the notification.
	"""

	title = models.CharField(max_length=200)
	"""
	Title of the notification.
	"""

	message = models.TextField(blank=True, default='')
	"""
	Message of the notification.
	"""

	object_type = models.CharField(max_length=100, db_index=True)
	"""
	Type of the referring object.
	"""

	object_key = models.CharField(max_length=200, null=True, default=None)
	"""
	Related key to object.
	"""

	object_data = JSONField(allow_null=True, default=None)
	"""
	Extra data of object.
	"""

	is_read = models.BooleanField(default=False)
	"""
	Is notification read.
	"""
