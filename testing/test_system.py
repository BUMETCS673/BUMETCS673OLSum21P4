import os
import sys
import HtmlTestRunner
import unittest
import time
import urllib
import urllib.request
import multiprocessing

sys.path.append("../app/")
from flask import request, url_for
from app import app, db, Admin, UserModel
from routes import *
from models import *
from selenium import webdriver
from datetime import datetime
from flask_testing import LiveServerTestCase

# Set test variables for test user and admin user
admin_username = "admin1"
admin_password = "admin1"
user_username = "st_test1"
user_password = "st_test1"
user_firstname = "st_test1Firstname"
user_lastname = "st_test1lastname"
user_email = "st_test1@123.com"


class SystemTesting(LiveServerTestCase):
    multiprocessing.set_start_method("fork")
    os_name = ''

    def create_app(self):
        # config_name = 'testing'
        # app = create_app(config_name)
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 8943
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../testing/test.db'

        return app

    def setUp(self):
        self.app = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()
            Admin.add_admin_user(self, 'John', 'Boyle', 'admin1@123.com', 'admin1', 'admin1')
            Admin.add_admin_user(self, 'Stephen', 'Best', 'admin2@123.com', 'admin2', 'admin2')
            user = UserModel(user_firstname, user_lastname, user_email, user_username, user_password, 'customer')
            user.set_password(user_password)
            user.add_user(user)
            db.session.commit()

        if SystemTesting.os_name.lower() == 'mac':
            self.driver = webdriver.Chrome(executable_path='../testing/Mac/chromedriver')
        elif SystemTesting.os_name.lower() == 'win':
            self.driver = webdriver.Chrome(executable_path='../testing/Window/chromedriver.exe')

        self.driver.get(self.get_server_url());



    def test_0_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def test_1_landing_page_ST_01(self):
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Welcome to MyDietHub')

    def test_2_home_page_ST_02(self):
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Welcome to MyDietHub')

    def test_3_about_page_ST_03(self):
        elem = self.driver.find_element_by_xpath('/html/body/header/nav/ul/li[2]/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'About MyDietHub')

    def test_4_login_page_ST_04(self):
        elem = self.driver.find_element_by_xpath('/html/body/header/nav/ul/li[3]/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h1')
        self.assertEqual(elem.text, 'Login')

    def test_5_logout_page_ST_05(self):
        elem = self.driver.find_element_by_xpath('/html/body/header/nav/ul/li[4]/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h1')
        self.assertEqual(elem.text, 'Login')

    def test_6_user_registration_ST_06(self):
        elem = self.driver.find_element_by_xpath('/html/body/header/nav/ul/li[3]/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/p/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h1')
        self.assertEqual(elem.text, 'Register')

        #Enter registration information
        firstname = self.driver.find_element_by_xpath('//*[@id="firstname"]')
        firstname.send_keys(user_firstname)
        lastname = self.driver.find_element_by_xpath('//*[@id="lastname"]')
        lastname.send_keys(user_lastname)
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys('ST_REGISTER')
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(user_password)
        email = self.driver.find_element_by_xpath('//*[@id="email"]')
        email.send_keys('STREGISTER@123.com')

        self.driver.find_element_by_xpath('/html/body/div[2]/h2/form/div[2]/input[6]').click()
        time.sleep(3)
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h1')
        #return to login page after registered successfully
        self.assertEqual(elem.text, 'Login')


    def test_7_login_page_ST_07(self):
        elem = self.driver.find_element_by_xpath('/html/body/header/nav/ul/li[3]/a').click()
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h1')
        self.assertEqual(elem.text, 'Login')

        #Enter login information
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys(user_username)
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(user_password)

        elem = self.driver.find_element_by_xpath('/html/body/div[2]/h2/form/input[3]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        #redirect the user to the 'Create a Meal' page (user's dashboard)
        self.assertEqual(elem.text, 'Enter Meal Details Below')


    def test_8_create_meal_ST_08(self):
        self.test_7_login_page_ST_07()
        time.sleep(2)
        #Enter the meal information
        self.driver.find_element_by_xpath('//*[@id="meal_type"]').send_keys('Dinner')
        self.driver.find_element_by_xpath('//*[@id="fitem1"]').send_keys("Beef")
        self.driver.find_element_by_xpath('//*[@id="fitem2"]').send_keys("noodle")

        self.driver.find_element_by_xpath('/html/body/div[2]/form[1]/input[4]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/p')
        #Meal is added successfully
        self.assertEqual(elem.text, 'Meal Added')


    def test_9_update_meal_ST_09(self):
        self.test_8_create_meal_ST_08()
        time.sleep(2)
        # Click 'View Meal' link
        self.driver.find_element_by_xpath('/html/body/div[2]/form[2]/button').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'List of Past Meals')

        # Click Update link
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[5]/a[2]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Update Meal Details Below')

        # Update the meal fields
        self.driver.find_element_by_xpath('//*[@id="meal_type"]').clear()
        self.driver.find_element_by_xpath('//*[@id="meal_type"]').send_keys("Lunch")
        self.driver.find_element_by_xpath('//*[@id="fitem1"]').clear()
        self.driver.find_element_by_xpath('//*[@id="fitem1"]').send_keys("pizza")
        self.driver.find_element_by_xpath('//*[@id="fitem2"]').clear()
        self.driver.find_element_by_xpath('//*[@id="fitem2"]').send_keys("apple")
        self.driver.find_element_by_xpath('/html/body/div[2]/form/input[4]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'List of Past Meals')

        # Validate the values in the update meal entry
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[1]')
        self.assertEqual(elem.text, "Lunch")
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[2]')
        self.assertEqual(elem.text, "pizza, apple")
        #elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[3]')
        #self.assertEqual(elem.text, "299.0")
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[4]')
        today = datetime.utcnow()
        self.assertEqual(elem.text, today.strftime('%m/%d/%Y'))

    def test_10_delete_meal_ST_10(self):
        self.test_8_create_meal_ST_08()
        time.sleep(2)
        # Click 'View Meal' link
        self.driver.find_element_by_xpath('/html/body/div[2]/form[2]/button').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'List of Past Meals')

        # Click Delete link
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[5]/a[1]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'List of Past Meals')

        # Validate the delete entry is gone
        elem = self.driver.find_element_by_xpath('/html/body/h3')
        self.assertEqual(elem.text, "There are no meals entered. Please create one.")

    def test_11_admin_login_ST_11(self):
        self.test_4_login_page_ST_04()
        username = self.driver.find_element_by_xpath('//*[@id="username"]')
        username.send_keys(admin_username)
        password = self.driver.find_element_by_xpath('//*[@id="password"]')
        password.send_keys(admin_password)

        self.driver.find_element_by_xpath('/html/body/div[2]/h2/form/input[3]').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Retrieve User Information')

    def test_12_admin_update_user_ST_12(self):
        self.test_11_admin_login_ST_10()
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_username)
        self.driver.find_element_by_xpath('/html/body/div[2]/form/button').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'User Details')

        #Update the user at User Details page
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[6]/a[2]').click()
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Update User Details Below')

        #update the user data
        update_firstname = user_username+'Update'
        update_lastname = user_lastname+'Update'
        update_username = user_username+'Update'
        update_password = user_password +'Update'
        update_email = 'st_test1Upate@123.com'
        self.driver.find_element_by_xpath('//*[@id="ufirstname"]').clear()
        self.driver.find_element_by_xpath('//*[@id="ulastname"]').clear()
        self.driver.find_element_by_xpath('//*[@id="uusername"]').clear()
        self.driver.find_element_by_xpath('//*[@id="upassword"]').clear()
        self.driver.find_element_by_xpath('//*[@id="uemail"]').clear()
        self.driver.find_element_by_xpath('//*[@id="ufirstname"]').send_keys(update_firstname)
        self.driver.find_element_by_xpath('//*[@id="ulastname"]').send_keys(update_lastname)
        self.driver.find_element_by_xpath('//*[@id="uusername"]').send_keys(update_username)
        self.driver.find_element_by_xpath('//*[@id="upassword"]').send_keys(update_password)
        self.driver.find_element_by_xpath('//*[@id="uemail"]').send_keys(update_email)
        self.driver.find_element_by_xpath('/html/body/div[2]/div/div/form/input[6]').click()

        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'User Details')

        #Validate the update user information
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[1]')
        self.assertEqual(elem.text, update_firstname)
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[2]')
        self.assertEqual(elem.text, update_lastname)
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[3]')
        self.assertEqual(elem.text, update_username)
        elem = self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[5]')
        self.assertEqual(elem.text, update_email)


    def test_13_admin_delete_user_ST_13(self):
        self.test_11_admin_login_ST_10()
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_username)
        self.driver.find_element_by_xpath('/html/body/div[2]/form/button').click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'User Details')

        #Delete user entry
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[6]/a[1]').click()
        time.sleep(3)
        elem = self.driver.find_element_by_xpath('/html/body/h1')
        self.assertEqual(elem.text, 'Retrieve User Information')


    def tearDown(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    #Validate the parameter
    if len(sys.argv) > 1:
        SystemTesting.os_name = sys.argv.pop()

    if SystemTesting.os_name.lower() != 'mac' and SystemTesting.os_name.lower() != 'win':
        print("ERROR : Not accept this parameter!")
        sys.exit()

    unittest.main(warnings='ignore', testRunner=HtmlTestRunner.HTMLTestRunner(output='test_result'))
