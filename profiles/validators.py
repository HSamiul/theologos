from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import datetime

def validate_dob(value):
    if (datetime.date.today() < value):
        raise ValidationError("Not a valid date of birth")
    return value

validate_phone = RegexValidator(
    regex=r'^(05)\d{9}$',
    message='Phone number must be entered in the format: 05999999999'
)