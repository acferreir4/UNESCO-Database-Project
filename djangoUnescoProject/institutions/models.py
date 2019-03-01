from django.db import models
from django.utils import timezone
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Country(models.Model):
    name = models.CharField(max_length=50)
    population = models.IntegerField()
    percent_indigenous = models.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )
    percent_gdp_on_ed = models.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )
    definition = models.CharField(max_length=50)
    average_education = models.CharField(max_length=50)
    strategy = models.CharField(max_length=50)
    continent = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=150)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    met = models.BooleanField(default=False)
    moc = models.BooleanField(default=False)
    ethics = models.BooleanField(default=False)
    status_request = models.BooleanField(default=False)
    ri_1_tools = models.DateField()
    #ri_1_tools = models.DateField(default=timezone.now)
    general = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    is_private = models.BooleanField(default=False)
    type_of_inst = models.CharField(max_length=50)
    student_count = models.IntegerField(validators=[MinValueValidator(0)])
    staff_count = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    internet_access = models.CharField(max_length=50, null=True, blank=True)
    online = models.CharField(max_length=50, null=True, blank=True)
    guest_lectures = models.CharField(max_length=50, null=True, blank=True)
    environment = models.CharField(max_length=50, null=True, blank=True)
    focus_pst = models.CharField(max_length=50, default='Not yet defined', null=True, blank=True)
    further = models.CharField(max_length=50, null=True, blank=True)
    school_size = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    community_size = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    girl_ratio = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)], 
            null=True, 
            blank=True
            )
    other_staff_count = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    qualifications = models.CharField(max_length=50, null=True, blank=True)
    percent_indigenous = models.FloatField(
            validators=[MinValueValidator(0), MaxValueValidator(100)], 
            null=True, 
            blank=True
            )
    age = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return self.name


class ResearchInstituteContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    function = models.CharField(max_length=150, null=True)
    degree = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name_plural = "Research Institution Contacts"

    def __str__(self):
        return f'{self.user.username} at {self.institution}'
