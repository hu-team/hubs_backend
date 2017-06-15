import datetime

import logging

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.cache.decorators import cache_response

from apps.absence.models import AbsenceReport
from apps.school.models import Lesson, Group, Presence, Course, Result
from apps.school import serializers
from django_filters.rest_framework import DjangoFilterBackend

from apps.school.serializers import LessonSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Lesson
	serializer_class = LessonSerializer
	queryset = Lesson.objects.all().select_related('teacher', 'course', 'group').prefetch_related('group__students')
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('course', 'group', 'teacher', 'id')
	ordering_fields = ('start', 'end')

	# def get_serializer_class(self):
	# 	if self.action == 'list':
	# 		return serializers.LessonSerializerLittle
	# 	return serializers.LessonSerializer

	def get_queryset(self):
		queryset = super().get_queryset()
		filter_from = datetime.datetime.utcnow()

		if self.request.user.is_teacher:
			queryset = queryset.filter(teacher=self.request.user.person)
		elif self.request.user.is_student:
			queryset = queryset.filter(group__in=self.request.user.person.groups.all())

		queryset = queryset.order_by('end')
		return queryset.filter(end__gte=filter_from)

	@cache_response(60 * 15)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Course
	queryset = Course.objects.all()
	serializer_class = serializers.CourseSerializer

	@cache_response(60 * 15)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Group
	queryset = Group.objects.all().prefetch_related('students')
	serializer_class = serializers.GroupSerializer

	def get_queryset(self):
		queryset = super().get_queryset()

		if self.request.user.is_student:
			queryset = queryset.filter(students=self.request.user.person_student)

		return queryset


class ResultViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Result
	queryset = Result.objects.all().prefetch_related('course', 'course__teachers').select_related('student')
	serializer_class = serializers.ResultSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('student',)

	def get_queryset(self):
		queryset = super().get_queryset()

		if self.request.user.is_student:
			queryset = queryset.filter(student=self.request.user.person_student)

		return queryset

	@cache_response(60 * 15)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class PresenceViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Presence
	queryset = Presence.objects.all()
	serializer_class = serializers.PresenceSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('lesson',)

	def get_queryset(self):
		queryset = super().get_queryset()

		if self.request.user.is_student:
			queryset = queryset.filter(student=self.request.user.person_student)

		return queryset

	def list(self, request, *args, **kwargs):
		if not self.request.user.is_student and 'lesson' in request.GET and 'prefill' in request.GET and request.GET['prefill']:
			try:
				lesson = Lesson.objects.select_related('group').prefetch_related('group__students').get(pk=request.GET['lesson'])
				lesson.prefill()
			except Exception as e:
				logging.exception(e)
				pass

		return super().list(request, *args, **kwargs)
