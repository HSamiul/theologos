from django.core.exceptions import ValidationError

'''
These validators are used in the `Post` and `Comment` models to ensure that a
post or comment is only able to be created and saved to the database if the
text is of a given minimum length (in this case, at least 30 characters).
'''

def validate_min_post_length(value):
    if len(value) < 30:
        raise ValidationError('Post must be at least 30 characters long.')

def validate_min_comment_length(value):
    if len(value) < 30:
        raise ValidationError('Comment must be at least 30 characters long.')
