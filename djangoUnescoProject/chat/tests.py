# chat/tests.py
from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.keys import Keys
#from seleniumlogin import force_login
from django.contrib.auth import get_user_model
from institutions.models import Institution, Country, City
from django.utils import timezone
from chat.models import ChatRooms, RoomAccess

class ChatTests(ChannelsLiveServerTestCase):
    serve_static = True  # emulate StaticLiveServerTestCase

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            # NOTE: Requires "chromedriver" binary to be installed in $PATH
            cls.driver = webdriver.Chrome(executable_path='/home/dhrubo/ENG4K/eecs_project/chat/chromedriver')
        except:
            super().tearDownClass()
            raise

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

# ==================================================================
# |               Integration Tests                                |
# ==================================================================

    def test_chat_Integration_testing(self):
        try:
            # makeing a tmp country, city and insttitutions for the users 
            countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
                definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
            countryCanada.save()
            cityToronto = City(name='Toronto', country=countryCanada)
            cityToronto.save()
            instUofT = Institution(name='University of Toronto', 
                                    city=cityToronto, 
                                    met=True, 
                                    moc=False, 
                                    ethics=True, 
                                    status_request=False, 
                                    ri_1_tools='2019-01-01', 
                                    general='OofT', 
                                    role='University', 
                                    is_private=False, 
                                    type_of_inst='University', 
                                    student_count=100, 
                                    staff_count=10)
            instUofT.save()
            User = get_user_model()
            # making main room
            main_room = ChatRooms.objects.create(name='Main_Room', 
                        category='G', display_line_1='Room for all', 
                        display_line_2='Members')

            # Making admin user
            user1 = User.objects.create_user(username='damini',
                                             password='test1234',
                                             institution=instUofT, is_staff=True, first_name='Damini', last_name='Taquori')
            # user1.is_staff=True
            # user1.save()
            # Making users
            user2 = User.objects.create_user(username='dhrubo',
                                             password='test1234',
                                             institution=instUofT, first_name='Shahriar', last_name='Dhrubo')

            # Loging user 1
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('damini')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/chat/Main_Room')
            time.sleep(3)

            self._open_new_window()
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('dhrubo')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/chat/Main_Room')
            time.sleep(3)

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value_sent,
                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value_replies,
                'Message was not received by window 2 from window 1')
            self._switch_to_window(0)
            self._post_message('I am downloading the chat..')
            time.sleep(2)
            download = self.driver.find_element_by_name('download_chat')

        finally:
            self._close_all_new_windows()



    # def test_non_admin_can_not_see_download_feature(self):
    #     try:
    #         # makeing a tmp country, city and insttitutions for the users 
    #         countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
    #             definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
    #         countryCanada.save()
    #         cityToronto = City(name='Toronto', country=countryCanada)
    #         cityToronto.save()
    #         instUofT = Institution(name='University of Toronto', 
    #                                 city=cityToronto, 
    #                                 met=True, 
    #                                 moc=False, 
    #                                 ethics=True, 
    #                                 status_request=False, 
    #                                 ri_1_tools='2019-01-01', 
    #                                 general='OofT', 
    #                                 role='University', 
    #                                 is_private=False, 
    #                                 type_of_inst='University', 
    #                                 student_count=100, 
    #                                 staff_count=10)
    #         instUofT.save()
    #         User = get_user_model()
    #         # making main room
    #         main_room = ChatRooms.objects.create(name='Main_Room', 
    #                     category='G', display_line_1='Room for all', 
    #                     display_line_2='Members')

    #         # Making admin user
    #         user1 = User.objects.create_user(username='damini',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         user1.save()
    #         # Loging user 1
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('damini')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/damini')

    #     finally:
    #         self._close_all_new_windows()


    # def test_admin_sees_download_feature(self):
    #     try:
    #         # makeing a tmp country, city and insttitutions for the users 
    #         countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
    #             definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
    #         countryCanada.save()
    #         cityToronto = City(name='Toronto', country=countryCanada)
    #         cityToronto.save()
    #         instUofT = Institution(name='University of Toronto', 
    #                                 city=cityToronto, 
    #                                 met=True, 
    #                                 moc=False, 
    #                                 ethics=True, 
    #                                 status_request=False, 
    #                                 ri_1_tools='2019-01-01', 
    #                                 general='OofT', 
    #                                 role='University', 
    #                                 is_private=False, 
    #                                 type_of_inst='University', 
    #                                 student_count=100, 
    #                                 staff_count=10)
    #         instUofT.save()
    #         User = get_user_model()
    #         # making main room
    #         main_room = ChatRooms.objects.create(name='Main_Room', 
    #                     category='G', display_line_1='Room for all', 
    #                     display_line_2='Members')

    #         # Making admin user
    #         user1 = User.objects.create_user(username='damini',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         user1.is_staff=True
    #         user1.save()
    #         # Loging user 1
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('damini')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/damini')
    #         self.assertEquals(self.driver.find_element_by_name('download_chat').text, 'DOWNLOAD CHAT')

    #     finally:
    #         self._close_all_new_windows()



    # def test_when_user_try_to_access_unauthorized_chat_session_and_gets_denied(self):
    #     try:
    #         # makeing a tmp country, city and insttitutions for the users 
    #         countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
    #             definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
    #         countryCanada.save()
    #         cityToronto = City(name='Toronto', country=countryCanada)
    #         cityToronto.save()
    #         instUofT = Institution(name='University of Toronto', 
    #                                 city=cityToronto, 
    #                                 met=True, 
    #                                 moc=False, 
    #                                 ethics=True, 
    #                                 status_request=False, 
    #                                 ri_1_tools='2019-01-01', 
    #                                 general='OofT', 
    #                                 role='University', 
    #                                 is_private=False, 
    #                                 type_of_inst='University', 
    #                                 student_count=100, 
    #                                 staff_count=10)
    #         instUofT.save()
    #         User = get_user_model()
    #         # making main room
    #         main_room = ChatRooms.objects.create(name='Main_Room', 
    #                     category='G', display_line_1='Room for all', 
    #                     display_line_2='Members')

    #         # Making users
    #         user1 = User.objects.create_user(username='damini',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         user2 = User.objects.create_user(username='safery',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         # Loging user 1
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('damini')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/damini')

    #         self._open_new_window()
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('safery')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/damini')

    #         self.assertEquals(self.driver.find_element_by_name('401_AC').text, '401 Unauthorized Error')

    #     finally:
    #         self._close_all_new_windows()


    # def test_when_chat_message_posted_then_seen_by_two_users_on_same_room(self):
    #     try:
    #         # makeing a tmp country, city and insttitutions for the users 
    #         countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
    #             definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
    #         countryCanada.save()
    #         cityToronto = City(name='Toronto', country=countryCanada)
    #         cityToronto.save()
    #         instUofT = Institution(name='University of Toronto', 
    #                                 city=cityToronto, 
    #                                 met=True, 
    #                                 moc=False, 
    #                                 ethics=True, 
    #                                 status_request=False, 
    #                                 ri_1_tools='2019-01-01', 
    #                                 general='OofT', 
    #                                 role='University', 
    #                                 is_private=False, 
    #                                 type_of_inst='University', 
    #                                 student_count=100, 
    #                                 staff_count=10)
    #         instUofT.save()
    #         User = get_user_model()
    #         # making main room
    #         main_room = ChatRooms.objects.create(name='Main_Room', 
    #                     category='G', display_line_1='Room for all', 
    #                     display_line_2='Members')

    #         # Making users
    #         user1 = User.objects.create_user(username='damini',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         user2 = User.objects.create_user(username='safery',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         # Loging user 1
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('damini')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/Main_Room')

    #         self._open_new_window()
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('safery')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/Main_Room')

    #         self._switch_to_window(0)
    #         self._post_message('hello')
    #         WebDriverWait(self.driver, 2).until(lambda _:
    #             'hello' in self._chat_log_value_sent,
    #             'Message was not received by window 1 from window 1')
    #         self._switch_to_window(1)
    #         WebDriverWait(self.driver, 2).until(lambda _:
    #             'hello' in self._chat_log_value_replies,
    #             'Message was not received by window 2 from window 1')
    #     finally:
    #         self._close_all_new_windows()

    # def test_two_joins_same_chat_session(self):
    #     try:
    #         # makeing a tmp country, city and insttitutions for the users 
    #         countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
    #             definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
    #         countryCanada.save()
    #         cityToronto = City(name='Toronto', country=countryCanada)
    #         cityToronto.save()
    #         instUofT = Institution(name='University of Toronto', 
    #                                 city=cityToronto, 
    #                                 met=True, 
    #                                 moc=False, 
    #                                 ethics=True, 
    #                                 status_request=False, 
    #                                 ri_1_tools='2019-01-01', 
    #                                 general='OofT', 
    #                                 role='University', 
    #                                 is_private=False, 
    #                                 type_of_inst='University', 
    #                                 student_count=100, 
    #                                 staff_count=10)
    #         instUofT.save()
    #         User = get_user_model()
    #         # making main room
    #         main_room = ChatRooms.objects.create(name='Main_Room', 
    #                     category='G', display_line_1='Room for all', 
    #                     display_line_2='Members')

    #         # Making users
    #         user1 = User.objects.create_user(username='damini',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         user2 = User.objects.create_user(username='safery',
    #                                          password='test1234',
    #                                          institution=instUofT)
    #         # Loging user 1
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('damini')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/Main_Room')

    #         self._open_new_window()
    #         self.driver.get(self.live_server_url + '/login/')
    #         username_field = self.driver.find_element_by_name('username')
    #         username_field.send_keys('safery')
    #         password_field = self.driver.find_element_by_name('password')
    #         password_field.send_keys('test1234')
    #         password_field.send_keys(Keys.RETURN)
    #         self.driver.get(self.live_server_url + '/chat/Main_Room')
    #     finally:
    #         self._close_all_new_windows()

# ==================================================================
# |                     Unit Tests                                 |
# ==================================================================

    # def test_home_page_status_code(self):
    #     response = self.client.get('/')
    #     self.assertEquals(response.status_code, 200)

    # def test_chat_page_status_code_200(self):
    #     response = self.client.get('/chat/')
    #     self.assertEquals(response.status_code, 200)

    # def test_chat_page_status_code_404(self):
    #     response = self.client.get('/chats/')
    #     self.assertEquals(response.status_code, 404)

    # def test_chat_Page_contains_discription(self):
    #     response = self.client.get('/chat/')
    #     self.assertContains(response, 'Go Back to the Home Page')

    # def test_chat_page_does_not_contain_incorrect_html(self):
    #     response = self.client.get('/')
    #     self.assertNotContains(
    #         response, 'Hi there! I should not be on the page.')


    # === Utility ===

    def _enter_chat_room(self, room_name):
        self.driver.get(self.live_server_url + '/chat/')
        ActionChains(self.driver).send_keys(room_name + '\n').perform()
        WebDriverWait(self.driver, 2).until(lambda _:
            room_name in self.driver.current_url)

    def _open_new_window(self):
        self.driver.execute_script('window.open("about:blank", "_blank");')
        self.driver.switch_to_window(self.driver.window_handles[-1])

    def _close_all_new_windows(self):
        while len(self.driver.window_handles) > 1:
            self.driver.switch_to_window(self.driver.window_handles[-1])
            self.driver.execute_script('window.close();')
        if len(self.driver.window_handles) == 1:
            self.driver.switch_to_window(self.driver.window_handles[0])

    def _switch_to_window(self, window_index):
        self.driver.switch_to_window(self.driver.window_handles[window_index])

    def _post_message(self, message):
        messageBox = self.driver.find_element_by_name('sendBox')
        messageBox.send_keys(message + '\n')
        # ActionChains(self.driver).send_keys(message + '\n').perform()

    @property
    def _chat_log_value_sent(self):
        # print(self.driver.find_element_by_xpath("//li[@class='sent']/p[1]").text)
        return self.driver.find_element_by_xpath("//li[@class='sent']/p[1]").text
    @property
    def _chat_log_value_replies(self):
        # print(self.driver.find_element_by_xpath("//li[@class='sent']/p[1]").text)
        return self.driver.find_element_by_xpath("//li[@class='replies']/p[1]").text

    @property
    def _get_401(self):
        print(self.driver.find_element_by_name('401_AC').text)
        return self.driver.find_element_by_name('401_AC')