

from rest_framework import serializers

from apps.core.models import User
from apps.school.models import Person


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'first_name', 'last_name', 'username',  # 'person',
		)
