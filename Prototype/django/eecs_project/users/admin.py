from django.contrib import admin
from .models import Region
from .models import Countries
from .models import Profile

# Register your models here.

admin.site.register(Region)
admin.site.register(Countries)
admin.site.register(Profile)