from django.contrib import admin
from django.forms import TextInput, Textarea, NumberInput
from django.db import models
from .models import Institution, City, Country, ResearchInstituteContact

class InstitutionModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'25'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size':'25'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

admin.site.register(Institution, InstitutionModelAdmin)
admin.site.register(City, InstitutionModelAdmin)
admin.site.register(Country, InstitutionModelAdmin)
admin.site.register(ResearchInstituteContact, InstitutionModelAdmin)
