import unittest
import sys

sys.path.append("../app/")
from flask import request, url_for
from app import app, db, Admin
from routes import *
from models import *


class RegistrationTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../testing/test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()
            Admin.add_admin_user(self, 'John', 'Boyle', 'admin1@123.com', 'admin1', 'admin1')
            Admin.add_admin_user(self, 'Stephen', 'Best', 'admin2@123.com', 'admin2', 'admin2')
            db.session.commit()

    def test_registration_page(self):
        response = self.app.get('/register', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        with self.app as client:
            response = client.post('/register',
                                   data=dict(firstname="testFirstname", lastname="testLastname", username="test1",
                                             password="test1", email="test@123.com"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert request.path == url_for('login')

    def test_username_exists(self):
        with self.app as client:
            response = client.post('/register',
                                    data=dict(firstname="testFirstname", lastname="testLastname", username="test1",
                                              password="test1", email="test1@123.com"), follow_redirects=True)

            response = client.post('/register',
                                   data=dict(firstname="testFirstname", lastname="testLastname", username="test1",
                                             password="test1", email="test1@123.com"), follow_redirects=True)

            self.assertTrue(b'Username is already exist' in response.data)

    def test_email_exists(self):
        with self.app as client:
            response = client.post('/register',
                                   data=dict(firstname="testFirstname", lastname="testLastname", username="test",
                                             password="test", email="test@123.com"), follow_redirects=True)

            response = client.post('/register',
                                   data=dict(firstname="testFirstname", lastname="testLastname", username="test2",
                                             password="test2", email="test@123.com"), follow_redirects=True)
            self.assertTrue(b'Email is already exist' in response.data)



    # def tearDown(self):
    #     with app.app_context():
    #         db.drop_all


if __name__ == "__main__":
    unittest.main()
