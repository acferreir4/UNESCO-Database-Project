from django import forms
from .models import Institution

class InstitutionCreateForm(forms.ModelForm):
    ri_1_tools = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Institution
        fields = ['name', 
                'city', 
                'met', 
                'moc', 
                'ethics', 
                'status_request', 
                'ri_1_tools', 
                'general', 
                'role', 
                'is_private', 
                'type_of_inst', 
                'student_count', 
                'staff_count'
                ]
