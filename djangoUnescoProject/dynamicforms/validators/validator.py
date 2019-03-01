from django.core.exceptions import ValidationError

def validate_field(value):
    if not value or ''.join(value.split()) == '':
        return 'This field must not be empty!'
    return ''