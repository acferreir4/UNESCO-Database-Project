import datetime
from django.test import TestCase
from institutions.models import City, Country, Institution
from django.core.exceptions import ValidationError


# Create your tests here.

class InstitutionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_string = 'testString'
        test_int = 99
        test_float = 90.9

        Country.objects.create(
                name = 'Canada',
                population = test_int,
                percent_indigenous = test_float,
                percent_gdp_on_ed = test_float,
                definition = test_string,
                average_education = test_string,
                strategy = test_string,
                continent = test_string,
                )

        City.objects.create(
                name = 'Toronto',
                country = Country.objects.get(id=1)
                )

        Institution.objects.create(
                name = 'York University',
                abbreviation = test_string,
                city = City.objects.get(id=1),
                ri_1_tools = datetime.date.today(),
                general = test_string,
                role = test_string,
                type_of_inst = test_string,
                student_count = test_int,
                )


    def test_country_name_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_country_name_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_country_population_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('population').verbose_name
        self.assertEquals(field_label, 'population')

    def test_country_population_greater_than_zero_validator(self):
        country = Country.objects.get(id=1)
        country.full_clean()
        with self.assertRaises(ValidationError):
            country.population = 0
            country.full_clean()

    def test_country_percent_indigenous_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('percent_indigenous').verbose_name
        self.assertEquals(field_label, 'Percentage of indigenous population')

    def test_country_percent_indigenous_validators(self):
        country = Country.objects.get(id=1)
        country.full_clean()
        with self.assertRaises(ValidationError):
            country.percent_indigenous = -1 
            country.full_clean()
        with self.assertRaises(ValidationError):
            country.percent_indigenous = 101
            country.full_clean()

    def test_country_percent_gdp_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('percent_gdp_on_ed').verbose_name
        self.assertEquals(field_label, 'Percentage of GDP spent on education')

    def test_country_percent_gdp_validators(self):
        country = Country.objects.get(id=1)
        country.full_clean()
        with self.assertRaises(ValidationError):
            country.percent_gdp_on_ed = -1 
            country.full_clean()
        with self.assertRaises(ValidationError):
            country.percent_gdp_on_ed = 101
            country.full_clean()

    def test_country_definition_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('definition').verbose_name
        self.assertEquals(field_label, 'definition')

    def test_country_definition_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('definition').max_length
        self.assertEquals(max_length, 50)

    def test_country_average_education_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('average_education').verbose_name
        self.assertEquals(field_label, 'Average level of education')

    def test_country_average_education_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('average_education').max_length
        self.assertEquals(max_length, 50)

    def test_country_strategy_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('strategy').verbose_name
        self.assertEquals(field_label, 'strategy')

    def test_country_strategy_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('strategy').max_length
        self.assertEquals(max_length, 50)

    def test_country_continent_label(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.get_field('continent').verbose_name
        self.assertEquals(field_label, 'continent')

    def test_country_continent_max_length(self):
        country = Country.objects.get(id=1)
        max_length = country._meta.get_field('continent').max_length
        self.assertEquals(max_length, 50)

    def test_country_plural_verbose_name(self):
        country = Country.objects.get(id=1)
        field_label = country._meta.verbose_name_plural
        self.assertEquals(field_label, 'Countries')



    def test_city_name_label(self):
        city = City.objects.get(id=1)
        field_label = city._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_city_name_max_length(self):
        city = City.objects.get(id=1)
        max_length = city._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_city_country_assignment(self):
        country = Country.objects.get(id=1)
        city = City.objects.get(id=1)
        self.assertEquals(country, city.country)


    def test_institution_name_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Name of institution')

    def test_institution_name_max_length(self):
        institution = Institution.objects.get(id=1)
        max_length = institution._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_institution_abbreviation_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('abbreviation').verbose_name
        self.assertEquals(field_label, 'abbreviation')

    def test_institution_abbreviation_max_length(self):
        institution = Institution.objects.get(id=1)
        max_length = institution._meta.get_field('abbreviation').max_length
        self.assertEquals(max_length, 15)

    def test_institution_city_assignment(self):
        institution = Institution.objects.get(id=1)
        city = City.objects.get(id=1)
        self.assertEquals(city, institution.city)

    def test_institution_moc_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('moc').verbose_name
        self.assertEquals(field_label, 'Memorandum of cooperation')

    def test_institution_moc_default_is_false(self):
        institution = Institution.objects.get(id=1)
        self.assertEquals(institution.moc, False)

    def test_institution_ethics_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('ethics').verbose_name
        self.assertEquals(field_label, 'Ethics approved')

    def test_institution_ethics_default_is_false(self):
        institution = Institution.objects.get(id=1)
        self.assertEquals(institution.ethics, False)

    def test_institution_private_label(self):
        institution = Institution.objects.get(id=1)
        field_label = institution._meta.get_field('is_private').verbose_name
        self.assertEquals(field_label, 'Private research institution')

    def test_institution_private_default_is_false(self):
        institution = Institution.objects.get(id=1)
        self.assertEquals(institution.is_private, False)

    def test_institution_student_count_validator(self):
        institution = Institution.objects.get(id=1)
        institution.student_count = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.student_count = -1
            institution.full_clean()

    def test_institution_staff_count_validator(self):
        institution = Institution.objects.get(id=1)
        institution.staff_count = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.staff_count = -1
            institution.full_clean()

    def test_institution_school_size_validator(self):
        institution = Institution.objects.get(id=1)
        institution.school_size = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.school_size = -1
            institution.full_clean()

    def test_institution_community_size_validator(self):
        institution = Institution.objects.get(id=1)
        institution.community_size = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.community_size = -1
            institution.full_clean()

    def test_institution_girl_ratio_validator(self):
        institution = Institution.objects.get(id=1)
        institution.girl_ratio = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.girl_ratio = -1
            institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.girl_ratio = 101
            institution.full_clean()

    def test_institution_percent_indigenous_validator(self):
        institution = Institution.objects.get(id=1)
        institution.percent_indigenous = 1
        institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.percent_indigenous = -1
            institution.full_clean()
        with self.assertRaises(ValidationError):
            institution.percent_indigenous = 101
            institution.full_clean()
