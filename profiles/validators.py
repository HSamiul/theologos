from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import datetime

def validate_dob(value):
    if (datetime.date.today() < value):
        raise ValidationError("Not a valid date of birth")
    return value

# TODO: Update validate_phone to accept all phone numbers and not 05-XXX-XXX-XXXX
validate_phone = RegexValidator(
    # source: https://ihateregex.io/expr/phone/
    regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
    message='Phone number must be a valid 10-digit US phone number.'
)