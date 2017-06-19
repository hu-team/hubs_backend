from rest_framework import serializers

from apps.school.models import StudentProgressIndexPoint


class StudentIndexPointSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudentProgressIndexPoint
		fields = ('student', 'period', 'school_year', 'complete', 'index', 'triggered', 'triggered_reason')
