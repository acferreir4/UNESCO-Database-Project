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

    def test_when_chat_message_posted_then_seen_by_two_users_on_same_room(self):
        try:
            # makeing a tmp country, city and insttitutions for the users 
            countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
                definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
            countryCanada.save()
            cityToronto = City(name='Toronto', country=countryCanada)
            cityToronto.save()
            instUofT = Institution(name='UofT', city=cityToronto, general='2nd best school after york', role='lean from york',
                type_of_inst='University', student_count=100000,staff_count=1000)
            instUofT.save()
            User = get_user_model()
            # Making users
            user1 = User.objects.create_user(username='damini',
                                             password='test1234',
                                             institution=instUofT)
            user2 = User.objects.create_user(username='safery',
                                             password='test1234',
                                             institution=instUofT)
            # Loging user 1
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('damini')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/login/')
            self._enter_chat_room('room_test_1')

            self._open_new_window()
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('safery')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/login/')
            self._enter_chat_room('room_test_1')

            self._switch_to_window(0)
            self._post_message('hello')
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value_sent,
                'Message was not received by window 1 from window 1')
            self._switch_to_window(1)
            WebDriverWait(self.driver, 2).until(lambda _:
                'hello' in self._chat_log_value_replies,
                'Message was not received by window 2 from window 1')
        finally:
            self._close_all_new_windows()

    def test_two_joins_same_chat_session(self):
        try:
            # makeing a tmp country, city and insttitutions for the users 
            countryCanada = Country(name='Canada', population='10000', percent_indigenous = '15', percent_gdp_on_ed='45',
                definition='This is main country', average_education='78%', strategy ='N/A', continent='North America')
            countryCanada.save()
            cityToronto = City(name='Toronto', country=countryCanada)
            cityToronto.save()
            instUofT = Institution(name='UofT', city=cityToronto, general='2nd best school after york', role='lean from york',
                type_of_inst='University', student_count=100000,staff_count=1000)
            instUofT.save()
            User = get_user_model()
            # Making users
            user1 = User.objects.create_user(username='damini',
                                             password='test1234',
                                             institution=instUofT)
            user2 = User.objects.create_user(username='safery',
                                             password='test1234',
                                             institution=instUofT)
            # Loging user 1
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('damini')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/login/')
            self._enter_chat_room('room_test_1')

            self._open_new_window()
            self.driver.get(self.live_server_url + '/login/')
            username_field = self.driver.find_element_by_name('username')
            username_field.send_keys('safery')
            password_field = self.driver.find_element_by_name('password')
            password_field.send_keys('test1234')
            password_field.send_keys(Keys.RETURN)
            self.driver.get(self.live_server_url + '/login/')
            self._enter_chat_room('room_test_1')
        finally:
            self._close_all_new_windows()



    # def test_when_chat_message_posted_then_not_seen_by_anyone_in_different_room(self):
    #     try:
    #         self._enter_chat_room('room_test_2')

    #         self._open_new_window()
    #         self._enter_chat_room('room_2')

    #         self._switch_to_window(0)
    #         self._post_message('hello')
    #         WebDriverWait(self.driver, 2).until(lambda _:
    #             'hello' in self._chat_log_value,
    #             'Message was not received by window 1 from window 1')

    #         self._switch_to_window(1)
    #         self._post_message('world')
    #         WebDriverWait(self.driver, 2).until(lambda _:
    #             'world' in self._chat_log_value,
    #             'Message was not received by window 2 from window 2')
    #         self.assertTrue('hello' not in self._chat_log_value,
    #             'Message was improperly received by window 2 from window 1')
    #     finally:
    #         self._close_all_new_windows()

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