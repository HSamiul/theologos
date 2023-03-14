from django.core.exceptions import ValidationError

def validate_min_post_length(value):
    if len(value) < 30:
        raise ValidationError('Post must be at least 30 characters long.')

def validate_min_comment_length(value):
    if len(value) < 30:
        raise ValidationError('Comment must be at least 30 characters long.')
