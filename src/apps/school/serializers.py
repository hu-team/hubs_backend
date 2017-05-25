from rest_framework import serializers

from apps.core.serializers import StudentSerializer, TeacherSerializer
from apps.school.models import Lesson, Group, Presence, Course


class LessonSerializer(serializers.ModelSerializer):

	teacher = TeacherSerializer()
	

	class Meta:
		model = Lesson
		fields = (
			'course', 'ignore_absence', 'teacher', 'group',
			'start', 'end',
		)


class CourseSerializer(serializers.ModelSerializer):

	class Meta:
		model = Course
		fields = (
			'code', 'name', 'ec_points'
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
		fields = (
			'present',
		)
