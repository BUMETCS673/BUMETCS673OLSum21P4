from app import app, db
import os
import unittest
from datetime import datetime

from models import MealModel

TEST_DB = 'test.db'

with app.app_context():

    class RouteTest(unittest.TestCase):
        def setUp(self):
            # app=create_app()
            with app.app_context():
                app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
                self.app = app.test_client(self)
                db.session.close()
            
                db.drop_all()
                db.create_all()

                self.assertEqual(app.debug, False)

        def test_home_page_route(self):
            response = self.app.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        def test_about_page_route(self):
            response = self.app.get('/about', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
        def test_food_input_route(self):
            response = self.app.get('/foodinput', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        def test_food_table_route(self):
            response = self.app.get('/foodtable', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

        def test_add_meal(self):
            response = self.app.post('/foodinput', data=dict(meal_type="Lunch", fitem1='Soup', fitem2='Apple' ), follow_redirects=True)
            self.assertTrue(b'Meal Added' in response.data)
    

if __name__ == '__main__':
    unittest.main()