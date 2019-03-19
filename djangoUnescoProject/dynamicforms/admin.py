from django.contrib import admin
from .models import DynamicForms, Questions, DataTable

admin.site.register(DynamicForms)
admin.site.register(Questions)
admin.site.register(DataTable)
