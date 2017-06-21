from rest_framework import serializers

from apps.core.serializers import StudentSerializer, TeacherSerializer, TeacherWithoutStudentSerializer, \
	StudentSerializerMinified
from apps.school.models import Lesson, Group, Presence, Course, Result
import random


class CourseSerializer(serializers.ModelSerializer):
	teachers = TeacherWithoutStudentSerializer(many=True, read_only=True)

	class Meta:
		model = Course
		fields = (
			'id', 'code', 'name', 'period', 'ec_points', 'teachers'
		)


class GroupSerializer(serializers.ModelSerializer):
	students = StudentSerializerMinified(
		many=True
	)

	class Meta:
		model = Group
		fields = (
			'id', 'code', 'school_year', 'students',
		)


class LessonSerializer(serializers.ModelSerializer):
	teacher = TeacherSerializer(read_only=True)
	course = CourseSerializer(read_only=True)
	group = GroupSerializer(read_only=True)
	room = serializers.SerializerMethodField()

	def get_room(self, obj):
		rooms = ['2.133', '0.053', '1.862', '3.153', '4.830']
		building_names = ['PL99', 'PL101', 'DL200', 'DL500']

		return random.choice(building_names) + '-' + random.choice(rooms)

	class Meta:
		model = Lesson
		fields = (
			'id', 'course', 'ignore_absence', 'teacher', 'group',
			'start', 'end', 'room'
		)


class LessonSerializerLittle(serializers.ModelSerializer):
	room = serializers.SerializerMethodField()
	def get_room(self, obj):
		rooms = ['2.133', '0.053', '1.862', '3.153', '4.830']
		building_names = ['PL99', 'PL101', 'DL200', 'DL500']

		return random.choice(building_names) + '-' + random.choice(rooms)

	class Meta:
		model = Lesson
		fields = (
			'id', 'course', 'ignore_absence', 'start', 'end', 'room'
		)


class PresenceSerializer(serializers.ModelSerializer):
	present = serializers.BooleanField(default=False)
	# TODO: Use nested serializer.
	absence_report = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Presence
		fields = (
			'id', 'lesson', 'student', 'present', 'absence_report'
		)


class ResultSerializer(serializers.ModelSerializer):

	course = CourseSerializer(read_only=True)
	course_id = serializers.IntegerField(write_only=True, required=True)
	student = StudentSerializerMinified(read_only=True)
	student_id = serializers.IntegerField(write_only=True, required=True)
	number_grade = serializers.IntegerField(required=False)
	ladder_grade = serializers.DecimalField(required=False, max_digits=2, decimal_places=1)

	class Meta:
		model = Result
		fields = (
			'id', 'course', 'course_id', 'student', 'student_id', 'ec_points', 'number_grade', 'ladder_grade', 'resit',
		)
