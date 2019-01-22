from django.db import models
from django.utils import timezone
from users.models import User


class Country(models.Model):
    name = models.CharField(max_length=50)
    population = models.IntegerField()
    percent_indigenous = models.FloatField()
    percent_gdp_on_ed = models.FloatField()
    definition = models.CharField(max_length=50)
    average_education = models.CharField(max_length=50)
    strategy = models.CharField(max_length=50)
    continent = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=150)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    met = models.BooleanField(default=False)
    moc = models.BooleanField(default=False)
    ethics = models.BooleanField(default=False)
    status_request = models.BooleanField(default=False)
    ri_1_tools = models.DateTimeField(default=timezone.now)
    general = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    is_private = models.BooleanField(default=False)
    type_of_inst = models.CharField(max_length=150)
    student_count = models.IntegerField()
    staff_count = models.IntegerField()

    def __str__(self):
        return self.name

class ResearchInstituteContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    function = models.CharField(max_length=150, null=True)
    degree = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f'{self.user.username} at {self.institution}'
