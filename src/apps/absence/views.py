from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.absence import serializers
from apps.absence.models import AbsenceReport


class AbsenceReportViewSet(viewsets.ModelViewSet):
	permission_classes = [IsAuthenticated]
	model = AbsenceReport
	queryset = AbsenceReport.objects.all()
	serializer_class = serializers.AbsenceReportSerializer
