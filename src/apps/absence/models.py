from django.db import models

from apps.core.models import BaseModel, User
from apps.school.models import Student


class AbsenceReport(BaseModel):
	TYPE_SICK = 'sick'
	TYPE_FAMILY = 'family'
	TYPE_OTHER = 'other'
	TYPE_CHOICES = (
		(TYPE_SICK, 'Sick'),
		(TYPE_FAMILY, 'Family Reasons'),
		(TYPE_OTHER, 'Other Reasons'),
	)

	student = models.ForeignKey(Student, related_name='absence_reports')
	"""
	Report to student (and reverse) connection.
	"""

	report_from = models.DateTimeField(
		null=False,
		auto_now_add=True,
	)
	"""
	The from date of the report.
	"""

	report_until = models.DateTimeField(
		null=True,
		default=None,
	)
	"""
	The until date of the report, None(null) when report is not yet closed and still valid to the student. (on-going).
	"""

	type = models.CharField(
		null=False,
		choices=TYPE_CHOICES,
		max_length=50,
	)
	"""
	Type of absence.
	"""

	reason = models.TextField(
		max_length=1000,
		null=True,
		blank=True,
		default=None,
	)
	"""
	Optional reason given by reporter.
	"""

	#

	created_by = models.ForeignKey(User, null=True, default=None, related_name='absence_reports_created')
	"""
	Report is created by this user.
	"""

	closed_by = models.ForeignKey(User, null=True, default=None, related_name='absence_reports_closed')
	""""
	Report is closed by this user.
	"""

