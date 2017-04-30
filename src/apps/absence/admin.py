from django.contrib import admin

from apps.absence.models import AbsenceReport


@admin.register(AbsenceReport)
class AbsenceReportAdmin(admin.ModelAdmin):
	icon = '<i class="material-icons">next_week</i>'
