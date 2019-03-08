from django.core.exceptions import ValidationError
from .models import DynamicForms

def validate_field(value):
    if not value or ''.join(value.split()) == '':
        return 'This field must not be empty!'
    return ''

def validate_title(title, form_pk):
    if form_pk and DynamicForms.object.get(id=form_pk) != title:
        return 'The title must be changed to a unique value or kept the same!'
    elif DynamicForms.objects.filter(title=title) and form_pk is None:
        return 'The title must be unique!'
    return ''