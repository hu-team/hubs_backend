import datetime
from rest_framework import serializers

from apps.absence.models import AbsenceReport
from apps.core.serializers import StudentSerializerMinified


class AbsenceReportSerializer(serializers.ModelSerializer):
	student = StudentSerializerMinified(read_only=True)
	student_id = serializers.IntegerField(write_only=True, required=True)
	report_from = serializers.DateTimeField(default=datetime.datetime.now(), required=False)
	type = serializers.ChoiceField(choices=AbsenceReport.TYPE_CHOICES, required=True)
	reason = serializers.CharField(max_length=1000, required=False, default=None)

	class Meta:
		model = AbsenceReport
		fields = ('id', 'student', 'student_id', 'report_from', 'report_until', 'type', 'reason')
