from rest_framework import serializers

from apps.school.models import Lesson, Group, Presence


class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lesson
		fields = (
			'course', 'ignore_absence', 'teacher', 'group',
			'start', 'end',
		)


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = (
			'code', 'school_year',
		)

class PresenceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Presence
		fields =(
			'present',
		)
