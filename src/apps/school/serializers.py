from rest_framework import serializers

from apps.core.serializers import StudentSerializer
from apps.school.models import Lesson, Group, Presence


class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lesson
		fields = (
			'course', 'ignore_absence', 'teacher', 'group',
			'start', 'end',
		)


class GroupSerializer(serializers.ModelSerializer):
	students = StudentSerializer(
		many=True
	)
	# students = serializers.HyperlinkedRelatedField(
	# 	view_name='core:students-detail', read_only=True,
	# 	many=True
	# )

	class Meta:
		model = Group
		fields = (
			'code', 'school_year', 'students',
		)


class PresenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Presence
		fields =(
			'present',
		)
