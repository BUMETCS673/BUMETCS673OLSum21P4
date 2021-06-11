from flask import Flask, json, render_template, url_for, jsonify, request, redirect
# from flask_cors import CORS
from datetime import datetime
from models import *

# instantiate a Flask application and store that in 'app'
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app)

app.secret_key = 'xf7\xc4\xfa\x91'

# config the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/data.db'
app.config['SQLALCHEMY_BINDS'] = {'two': 'sqlite:///../database/meal.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

user = UserModel()
admin = Admin()
db.init_app(app)  # initalize db
with app.app_context():
    db.create_all()
    admin.add_admin_user('John', 'Boyle', 'admin1@123.com', 'admin1', 'admin1')
    admin.add_admin_user('Stephen', 'Best', 'admin2@123.com', 'admin2', 'admin2')
    # db.create_all(bind='two')
    db.session.commit()

# import declared routes
import routes

if __name__ == "__main__":
    app.run(debug=True)
