from rest_framework import serializers

from apps.school.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lesson
		fields = (
			'course', 'ignore_absence', 'teacher', 'group',
			'start', 'end',
		)
