from django.db import models
from django.core.validators import RegexValidator

from ..accounts.models import User

class Profile(models.Model):
    '''
    Extend the `User` model using a one-to-one association to this `Profile`
    model. The main responsibility of this class is to hold user information
    unrelated to authentication.
    '''

    # Each `Profile` has one `User` and each `User` has one `Profile`
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)

    # TODO: Figure out how to save images.
    # Each `Profile` may have a profile photo to display next to profile's
    # comments.
    # profile_photo = models.ImageField(blank=True)

    # Each `Profile` may have a date of birth so that the commentaries they see
    # can be tailored to their age group.
    dob = models.DateField(blank=True)
    
    class FaithTradition(models.TextChoices):
        '''
        An enumeration type which defines choices of faith tradition. More
        faith traditions may be added in the future.
        '''
        BAPTIST = 'BAPT', 'Baptist'
        PENTECOSTAL = 'PENT', 'Pentecostal'
        AGNOSTIC = 'AGN', 'Agnostic'
    
    # Each `Profile` keeps track of the faith tradition of the user. This will
    # be used so that users can filter the comments they see based on the 
    # faith tradition of the authors of the comments.
    faith_tradition = models.CharField(choices=FaithTradition.choices)

    # Error message when a wrong format entered.
    phone_message = 'Phone number must be entered in the format: 05999999999' 

    # The desired format for entering phone number.
    phone_regex = RegexValidator(
        regex=r'^(05)\d{9}$',
        message=phone_message
    )

    # Each `Profile` contains an optional phone number field that is validated
    # against a regex.
    phone = models.CharField(validators=[phone_regex], max_length=60,
                             null=True, blank=True)