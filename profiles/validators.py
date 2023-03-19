from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import datetime

def validate_dob(value):
    if (datetime.date.today() < value):
        raise ValidationError("Not a valid date of birth")
    return value

# TODO: Update validate_phone to accept all phone numbers and not 05-XXX-XXX-XXXX
validate_phone = RegexValidator(
    regex=r'^(05)\d{9}$',
    message='Phone number must be entered in the format: 05999999999'
)