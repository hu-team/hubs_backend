import datetime

import logging

from django.utils.timezone import now
from rest_framework import viewsets, views
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework_extensions.cache.decorators import cache_response

from apps.absence.models import AbsenceReport
from apps.core.permissions import ReadOnlyOrWriteAccess
from apps.school.models import Lesson, Group, Presence, Course, Result
from apps.school import serializers
from django_filters.rest_framework import DjangoFilterBackend

from apps.school.serializers import LessonSerializer


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
	model = Lesson
	serializer_class = LessonSerializer
	queryset = Lesson.objects.all().select_related('teacher', 'course', 'group').prefetch_related('group__students')
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

	@cache_response(60 * 15)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
	model = Course
	queryset = Course.objects.all()
	serializer_class = serializers.CourseSerializer

	@cache_response(60 * 15)
	def list(self, request, *args, **kwargs):
		return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
	model = Group
	queryset = Group.objects.all().prefetch_related('students')
	serializer_class = serializers.GroupSerializer

	def get_queryset(self):
		queryset = super().get_queryset()

		if self.request.user.is_student:
			queryset = queryset.filter(students=self.request.user.person_student)

		return queryset


class ResultViewSet(viewsets.ModelViewSet):
	permission_classes = [ReadOnlyOrWriteAccess]
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
	permission_classes = [ReadOnlyOrWriteAccess]
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


class LessonPresenceOverviewView(views.APIView):
	def get(self, request, lesson_pk, *args, **kwargs):
		if not request.user or not request.user.is_teacher:
			raise PermissionDenied(detail='User is not allowed to call this route!')

		try:
			lesson = Lesson.objects.select_related('group').get(pk=lesson_pk)

			# Get previous lessons.
			previous_lessons = lesson.course.lessons.filter(
				start__lte=lesson.start,
				group=lesson.group,
			).order_by('-start')[:5]
			previous_lessons = previous_lessons.reverse()
		except Lesson.DoesNotExist:
			raise NotFound(detail='Lesson not found!')

		group = lesson.group
		data = list()

		for student in group.students.all():
			row = dict(
				id=student.id,
				name=student.full_name,
				lessons=list()
			)

			# Get previous and current lesson presence.
			for lesson in previous_lessons:
				if lesson.presence_set.count() < group.students.count():
					lesson.prefill()

				lesson_presence = student.presence_set.filter(lesson=lesson).first()
				row['lessons'].append(dict(
					id=lesson.id,
					start=lesson.start.isoformat(),
					end=lesson.end.isoformat(),
					presence=lesson_presence.present if lesson_presence else None,
					absence_type=lesson_presence.absence_report.type if lesson_presence and lesson_presence.absence_report else None
				))

			data.append(row)

		return Response(data)
