import datetime
from django.test import TestCase
from django.urls import reverse
from users.models import User
from institutions.models import City, Country, Institution


class RegisterViewTest(TestCase):
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

        User.objects.create(
                username = 'admin',
                institution = Institution.objects.get(id=1),
                is_staff = True,
                password = 'testing987',
                )
        
        User.objects.create(
                username = 'notAdmin',
                institution = Institution.objects.get(id=1),
                is_staff = False,
                password = 'testing987',
                )

    def test_register_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/register/')

    def test_non_admin_logged_in_denied_registration(self):
        login = self.client.login(username='notAdmin', password='testing987')
        response = self.client.get(reverse('register'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'notAdmin')
        # Check that we got a redirection
        self.assertEqual(response.status_code, 302)
        # Check we used correct template
        self.assertTemplateUsed(response, 'users/access_denied.html')

    def test_admin_logged_in_uses_correct_template(self):
        login = self.client.login(username='admin', password='testing987')
        response = self.client.get(reverse('register'))
        
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'users/register.html')
