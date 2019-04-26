# can run this in django shell with following command:
# exec(open('scripts/populateDb.py').read())

import json
from institutions.models import Country, City, Institution 
from users.models import User
from chat.models import ChatRooms

with open('scripts/countries.json') as f_countries:
    countries_json = json.load(f_countries)

for country in countries_json:
    country = Country( 
            name=country['name'], 
            population=country['population'], 
            percent_indigenous=country['percent_indigenous'], 
            percent_gdp_on_ed=country['percent_gdp_on_ed'], 
            definition=country['definition'], 
            average_education=country['average_education'], 
            strategy=country['strategy'], 
            continent=country['continent']
            )
    country.save()

with open('scripts/cities.json') as f_cities:
    cities_json = json.load(f_cities)

for city in cities_json:
    city = City(
            name=city['name'], 
            country_id=city['country_id']
            )
    city.save()

with open('scripts/institutions.json') as f_institutions:
    institutions_json = json.load(f_institutions)

for inst in institutions_json:
    inst = Institution(
            name=inst['name'], 
            city_id=inst['city_id'], 
            met=inst['met'], 
            moc=inst['moc'], 
            ethics=inst['ethics'], 
            status_request=inst['status_request'], 
            ri_1_tools=inst['date'], 
            general=inst['general'], 
            role=inst['role'], 
            is_private=inst['is_private'], 
            type_of_inst=inst['type_of_inst'], 
            student_count=inst['student_count'], 
            staff_count=inst['staff_count']
            )
    inst.save()

MainRoom = ChatRooms(
        name='Main_Room',
    	category='G',
    	display_line_1='Discussion Board',
    	display_line_2='For All Members'
        )
MainRoom.save()

user = User(
        username='admin', 
        first_name='Andrew', 
        last_name='Ferreira',
        email='admin@admin.com',
        is_staff=True,
        is_active=True,
        is_superuser=True,
        role='Administrator',
        institution_id = 1
        )
user.set_password('testing321')
user.save()

