from django.contrib import admin
from .models import Institution, City, Country, ResearchInstituteContact

admin.site.register(Institution)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(ResearchInstituteContact)
