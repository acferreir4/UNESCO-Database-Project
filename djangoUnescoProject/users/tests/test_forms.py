import datetime

from django.test import TestCase
from django.utils import timezone

from users.models import User
from institutions.models import City, Country, Institution
from users.forms import UserRegisterForm, UserUpdateForm

class UserRegisterFormTest(TestCase):
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

    def test_register_form_username_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['username'].label == None or 
                form.fields['username'].label == 'Username'
                )

    def test_register_form_first_name_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['first_name'].label == None or 
                form.fields['first_name'].label == 'First name'
                )

    def test_register_form_last_name_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['last_name'].label == None or 
                form.fields['last_name'].label == 'Last name'
                )

    def test_register_form_email_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['email'].label == None or 
                form.fields['email'].label == 'Email'
                )

    def test_register_form_staff_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['is_staff'].label == None or 
                form.fields['is_staff'].label == 'Staff status'
                )

    def test_register_form_role_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['role'].label == None or 
                form.fields['role'].label == 'Role'
                )

    def test_register_form_institution_label(self):
        form = UserRegisterForm()
        self.assertTrue(
                form.fields['institution'].label == None or 
                form.fields['institution'].label == 'Institution'
                )

    def test_register_form_username_helptext(self):
        form = UserRegisterForm()
        self.assertEquals(
                form.fields['username'].help_text,
                'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
                )
