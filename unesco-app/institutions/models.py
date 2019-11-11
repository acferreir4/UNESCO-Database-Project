from django.db import models
from django.utils import timezone
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Country(models.Model):
    name = models.CharField(max_length=50)
    population = models.IntegerField(validators=[MinValueValidator(1)])
    percent_indigenous = models.FloatField(
            'Percentage of indigenous population',
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )
    percent_gdp_on_ed = models.FloatField(
            'Percentage of GDP spent on education',
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )
    definition = models.CharField(max_length=50)
    average_education = models.CharField('Average level of education', max_length=50)
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
    name = models.CharField('Name of institution', max_length=150)
    abbreviation = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    met = models.BooleanField(default=False)
    moc = models.BooleanField('Memorandum of cooperation', default=False)
    ethics = models.BooleanField('Ethics approved', default=False)
    status_request = models.BooleanField(default=False)
    is_private = models.BooleanField('Private research institution', default=False)
    ri_1_tools = models.DateField()

    general_choices = (
        ("passive", "Passive"),
        ("active", "Active"),
    )
    general = models.CharField(max_length=10, choices=general_choices, blank=True, default="active")

    role_choices = (
        ("research", "Research"),
        ("coordination", "Coordination"),
        ("government", "Government"),
    )
    role = models.CharField(max_length=15, choices=role_choices, default="research")

    inst_choices = (
        ("university", "University"),
        ("ngo", "NGO"),
        ("college", "College"),
        ("rce", "RCE"),
    )
    type_of_inst = models.CharField('Type of institution', max_length=15, choices=inst_choices, default="university")

    student_count = models.IntegerField(validators=[MinValueValidator(0)])

    staff_count = models.IntegerField(validators=[MinValueValidator(0)])

    internet_choices = (
        ("yes", "Yes"),
        ("none", "None"),
        ("seldom", "Seldom"),
    )
    internet_access = models.CharField(max_length=10, choices=internet_choices, blank=True, default="yes")

    online_choices = (
        ("yes", "Yes"),
        ("none", "None"),
        ("seldom", "Seldom"),
        ("often", "Often"),
    )
    online = models.CharField('Use of online learning material', max_length=10, choices=online_choices, blank=True, default="yes")

    guest_choices = (
        ("often", "Often"),
        ("frequently", "Frequently"),
        ("seldom", "Seldom"),
        ("never", "Never"),
    )
    guest_lectures = models.CharField(max_length=15, choices=guest_choices, blank=True, default="never")

    env_choices = (
        ("often", "Often"),
        ("frequently", "Frequently"),
        ("seldom", "Seldom"),
        ("never", "Never"),
    )
    environment = models.CharField(max_length=15, choices=env_choices, blank=True, default="never")

    pst_choices = (
        ("all", "All"),
        ("primary", "Primary"),
        ("secondary", "Secondary"),
        ("tertiary", "Tertiary"),
        ("kindergarten", "Kindergarten"),
        ("undefined", "Not yet defined"),
    )
    focus_pst = models.CharField('Focus on K/P/S/T', max_length=15, choices=pst_choices, blank=True, default="undefined")

    further = models.CharField('Further levels of education', max_length=50, blank=True, default="")

    school_size = models.IntegerField(
            validators=[MinValueValidator(0)], 
            null=True, 
            blank=True
            )

    community_size = models.IntegerField(
            validators=[MinValueValidator(0)], 
            null=True, 
            blank=True
            )

    girl_ratio = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)], 
            null=True, 
            blank=True
            )

    qual_choices = (
        ("bachelor", "Bachelor"),
        ("master", "Master"),
        ("phd", "PhD"),
        ("certificate", "Certificate"),
    )
    qualifications = models.CharField(max_length=15, choices=qual_choices, blank=True, default="bachelor")

    percent_indigenous = models.FloatField(
            'Percentage of indigenous students',
            validators=[MinValueValidator(0), MaxValueValidator(100)], 
            null=True, 
            blank=True
            )

    age = models.IntegerField(
            'Average age', 
            validators=[MinValueValidator(0)], 
            null=True, 
            blank=True
            )

    def __str__(self):
        return self.name


class ResearchInstituteContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    function = models.CharField(max_length=150, blank=True)

    degree_choices = (
        ("phd", "PhD"),
        ("master", "Master"),
        ("bachelor", "Bachelor"),
    )
    degree = models.CharField(max_length=10, choices=degree_choices, blank=True, default="bachelor")

    class Meta:
        verbose_name_plural = "Research Institution Contacts"

    def __str__(self):
        return f'{self.user.username} at {self.institution}'
