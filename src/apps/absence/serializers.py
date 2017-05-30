from rest_framework import serializers

from apps.absence.models import AbsenceReport
from apps.core.serializers import StudentSerializer


class AbsenceReportSerializer(serializers.ModelSerializer):
	student = StudentSerializer(read_only=True)

	class Meta:
		model = AbsenceReport
		fields = ('id', 'student', 'report_from', 'report_until', 'type', 'reason')
