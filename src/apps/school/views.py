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


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Lesson
	queryset = Lesson.objects.all().prefetch_related('teacher', 'course', 'group', 'group__students')
	serializer_class = serializers.LessonSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('course', 'group', 'teacher', 'id')
	ordering_fields = ('start', 'end')

	def get_queryset(self):
		queryset = super().get_queryset()
		filter_from = datetime.datetime.utcnow()

		if self.request.user.is_teacher:
			queryset = queryset.filter(teacher=self.request.user.person)
		elif self.request.user.is_student:
			queryset = queryset.filter(group__in=self.request.user.person.groups.all())

		queryset = queryset.order_by('end')
		return queryset.filter(end__gte=filter_from)


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


class ResultViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Result
	queryset = Result.objects.all().prefetch_related('course', 'course__teachers').select_related('student')
	serializer_class = serializers.ResultSerializer


class PresenceViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Presence
	queryset = Presence.objects.all()
	serializer_class = serializers.PresenceSerializer
	filter_backends = (DjangoFilterBackend,)
	filter_fields = ('lesson',)

	def prefill(self, lesson):
		"""
		:param lesson: Lesson instance
		:type lesson: apps.school.models.Lesson
		"""
		for student in lesson.group.students.all():
			report = AbsenceReport.objects.filter(
				Q(student=student) & Q(report_from__lte=lesson.start) & Q(
					Q(report_until__isnull=True) | Q(report_until__gte=lesson.start)
				)
			).first()

			Presence.objects.get_or_create(
				lesson=lesson,
				student=student,
				defaults=dict(
					absence_report=report,
					present=False
				)
			)

	def list(self, request, *args, **kwargs):
		if 'lesson' in request.GET and 'prefill' in request.GET and request.GET['prefill']:
			try:
				lesson = Lesson.objects.select_related('group').prefetch_related('group__students').get(pk=request.GET['lesson'])
				self.prefill(lesson)
			except Exception as e:
				logging.exception(e)
				pass

		# if self.request.query_params.get
		return super().list(request, *args, **kwargs)
