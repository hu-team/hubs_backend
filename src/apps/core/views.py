from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.core.models import User
from apps.school.models import Student, Teacher
from . import serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = User
	queryset = User.objects.all().select_related('person_student', 'person_teacher')
	serializer_class = serializers.UserApiSerializer


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Student
	queryset = Student.objects.all().select_related('user')
	serializer_class = serializers.StudentSerializer


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Teacher
	queryset = Teacher.objects.all().select_related('user')
	serializer_class = serializers.TeacherSerializer
