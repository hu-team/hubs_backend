import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.school.models import Lesson, Group, Presence
from apps.school import serializers


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Lesson
	queryset = Lesson.objects.all()
	serializer_class = serializers.LessonSerializer
	filter_fields = ('course', 'group', 'teacher')
	ordering_fields = ('start', 'end')

	def get_queryset(self):
		# TODO: Date filtering.
		# filter_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

		if self.request.user.is_teacher:
			return Lesson.objects.filter(teacher=self.request.user.person)
		elif self.request.user.is_student:
			return Lesson.objects.filter(group__in=self.request.user.person.groups.all())


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Group
	queryset = Group.objects.all()
	serializer_class =  serializers.GroupSerializer

class PresenceViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Presence
	queryset = Presence.objects.all()
	serializer_class = serializers.PresenceSerializer
