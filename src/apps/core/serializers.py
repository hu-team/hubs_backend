from rest_framework import serializers

from apps.core.models import User
from apps.school.models import Student, Teacher, StudentProgressIndexPoint
from apps.stats.serializers import StudentIndexPointSerializer


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'first_name', 'last_name', 'username',  # 'person',
		)


class UserApiSerializer(serializers.ModelSerializer):
	user_type = serializers.SerializerMethodField()
	student_id = serializers.SerializerMethodField()
	teacher_id = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'user_type',
			'student_id', 'teacher_id'
		)

	def get_student_id(self, obj):
		if obj.is_student:
			return obj.person.pk
		return None

	def get_teacher_id(self, obj):
		if obj.is_teacher:
			return obj.person.pk
		return None

	def get_user_type(self, obj):
		if obj.is_counselor:
			return 'counselor'
		elif obj.is_teacher:
			return 'teacher'
		elif obj.is_student:
			return 'student'
		return 'unknown'


class CounselorSerializer(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()

	class Meta:
		model = Teacher
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email'
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email


class StudentSerializer(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	last_index_point = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Student
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'student_number', 'graduated', 'last_index_point'
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email

	def get_last_index_point(self, obj):
		last_index = StudentProgressIndexPoint.objects.filter(
			student=obj, complete=True
		).order_by('school_year', 'period').last()
		print(last_index)

		if last_index:
			return StudentIndexPointSerializer(last_index).data
		return None


class StudentSerializerWithCounselor(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	counselor = CounselorSerializer(read_only=True)
	last_index_point = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = Student
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'student_number', 'graduated', 'counselor', 'last_index_point'
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email

	def get_last_index_point(self, obj):
		last_index = StudentProgressIndexPoint.objects.filter(
			student=obj, complete=True
		).order_by('school_year', 'period').last()

		if last_index:
			return StudentIndexPointSerializer(last_index).data
		return None


class StudentSerializerMinified(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()

	class Meta:
		model = Student
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'student_number', 'graduated',
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email


class TeacherWithoutStudentSerializer(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	user_type = serializers.SerializerMethodField()

	class Meta:
		model = Teacher
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'user_type',
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email

	def get_user_type(self, obj):
		if obj.is_counselor:
			return 'counselor'
		else:
			return 'teacher'


class TeacherSerializer(serializers.ModelSerializer):
	first_name = serializers.SerializerMethodField()
	last_name = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	email = serializers.SerializerMethodField()
	user_type = serializers.SerializerMethodField()
	students = StudentSerializer(read_only=True, many=True)

	class Meta:
		model = Teacher
		fields = (
			'id', 'first_name', 'last_name', 'username', 'email', 'user_type', 'students'
		)

	def get_first_name(self, obj):
		return obj.user.first_name

	def get_last_name(self, obj):
		return obj.user.last_name

	def get_username(self, obj):
		return obj.user.username

	def get_email(self, obj):
		return obj.user.email

	def get_user_type(self, obj):
		if obj.is_counselor:
			return 'counselor'
		else:
			return 'teacher'


class MailSerializer(serializers.Serializer):
	subject = serializers.CharField(max_length=50)
	message = serializers.CharField(max_length=500)
	to_email = serializers.EmailField()

	class Meta:
		fields = (
			'subject', 'message', 'to_email',
		)
