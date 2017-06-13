import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_school_year(value):
	match = re.search(r'^([2][0-9]{3})-([2][0-9]{3})$', value)
	if not match or len(match.groups()) != 2:
		raise ValidationError(
			_('%(value)s is not a valid school year, (2016-2017 would be valid)'),
			params={'value': value}
		)

	start_year = int(match.group(1))
	end_year = int(match.group(2))

	if not end_year - start_year == 1:
		raise ValidationError(
			_('%(value)s is not covering a single school year!'),
			params={'value': value}
		)
