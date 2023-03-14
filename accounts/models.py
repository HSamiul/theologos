from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    '''
    A `User` model implementing the Django built-in AbstractUser model. The
    main responsibility of this class is to take care of authentication and
    authorization.
    '''

    # Each `User` has a human-readable unique identifier. Indexing this field
    # provides faster lookup time.
    username = models.CharField(max_length=150, unique=True, db_index=True)
    
    # Each `User` is required to have a first name to display on their profile.
    first_name = models.CharField(max_length=150)

    # Each `User` is required to have a last name to display on their profile.
    last_name = models.CharField(max_length=150)

    # Each `User` is required to have an email address in order for the 
    # application to contact users during login.
    email = models.EmailField(db_index=True, unique=True)

    # The `is_active` flag designates whether the user is active or not. For
    # example, when a user is banned or wants to delete their account, 
    # `is_active` should be set to false.
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag designates whether this user can access the admin 
    # site.
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        '''
        Returns the username as a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        '''

        return self.username
