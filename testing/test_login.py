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
            db.session.commit()

    def test_user_login(self):
        with self.app as client:
            response = client.post('/register',
                                   data=dict(firstname="testFirstname", lastname="testLastname", username="test",
                                             password="test", email="test@123.com"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert request.path == url_for('login')

            response = client.post('/login', data=dict(username="test", password="test"),
                                   follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert request.path == url_for('foodinput')

    def test_incorrect_username_login(self):
        with self.app as client:
            response = client.post('/login', data=dict(username="test1", password="test"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert (b'Incorrect username!' in response.data)

    def test_incorrect_password_login(self):
        with self.app as client:
            response = client.post('/login', data=dict(username="test", password="test1"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert (b'Incorrect username!' in response.data)

    def test_incorrect_username_password_login(self):
        with self.app as client:
            response = client.post('/login', data=dict(username="test1", password="test1"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert (b'Incorrect username!' in response.data)

    def test_incorrect_username_password_login(self):
        with self.app as client:
            response = client.post('/login', data=dict(username="test1", password="test1"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert (b'Incorrect username!' in response.data)

    def test_unregistered_user_login(self):
        with self.app as client:
            response = client.post('/login', data=dict(username="testr", password="testr"), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            assert (b'Incorrect username!' in response.data)


if __name__ == "__main__":
    unittest.main()
