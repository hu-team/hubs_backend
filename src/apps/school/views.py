import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.school.models import Lesson
from apps.school import serializers


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
	permission_classes = [IsAuthenticated]
	model = Lesson
	queryset = Lesson.objects.all()
	serializer_class = serializers.LessonSerializer
	filter_fields = ('course', 'group', 'teacher')
	ordering_fields = ('start', 'end')

	def get_queryset(self):
		queryset = super().get_queryset()

		filter_from = datetime.datetime.now()

		if self.request.user.is_teacher:
			queryset = queryset.filter(teacher=self.request.user.person)
		elif self.request.user.is_student:
			queryset = queryset.filter(group__in=self.request.user.person.groups.all())

		return queryset.filter(end__lte=filter_from)
