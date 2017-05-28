import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.school.models import Lesson, Group, Presence, Course
from apps.school import serializers
from django_filters.rest_framework import DjangoFilterBackend


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Lesson
	queryset = Lesson.objects.all().prefetch_related('teacher', 'course')
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


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Group
	queryset = Group.objects.all().prefetch_related('students')
	serializer_class = serializers.GroupSerializer


class PresenceViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Presence
	queryset = Presence.objects.all()
	serializer_class = serializers.PresenceSerializer
