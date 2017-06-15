from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.absence import serializers
from apps.absence.models import AbsenceReport
from apps.core.permissions import StudentReadOnlyAndPost


class AbsenceReportViewSet(viewsets.ModelViewSet):
	permission_classes = [StudentReadOnlyAndPost]
	model = AbsenceReport
	queryset = AbsenceReport.objects.all()
	serializer_class = serializers.AbsenceReportSerializer
