from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.school.models import StudentProgressIndexPoint
from . import serializers


class StudentStatistics(
	mixins.RetrieveModelMixin,
	mixins.ListModelMixin,
	viewsets.GenericViewSet
):
	permission_classes = [IsAuthenticated]
	model = StudentProgressIndexPoint
	queryset = StudentProgressIndexPoint.objects.all().order_by('-school_year', '-period')
	serializer_class = serializers.StudentIndexPointSerializer
	lookup_field = 'student_id'

	def get_queryset(self):
		if 'student_id' not in self.kwargs:
			return super().get_queryset().none()
		if self.request.user.is_student:
			return super().get_queryset().filter(student=self.request.user.person)
		return super().get_queryset().filter(student_id=self.kwargs['student_id'])

	def retrieve(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
