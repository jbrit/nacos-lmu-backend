import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def year_2xxx_validator(year):
    if year < 2000 or year >= 2999:
        raise ValidationError(
            _('%(value)s is not a valid year in this millenium'),
            params={'value': year},
        )

def course_code_validator(course_code: str):
    if not re.match("^[A-Z]{3} \d{3}$",course_code):
        raise ValidationError(
            _('%(value)s is not in the format: CSC 999'),
            params={'value': course_code},
        )