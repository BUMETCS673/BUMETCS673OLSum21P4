# app.py - This app will allow for entry of specific meals and thier associated food items.

from flask import Flask, json, render_template, url_for, jsonify, request, redirect
from flask_cors import CORS

from datetime import datetime
from models import db, MealModel

# instantiate a Flask application and store that in 'app'
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

app.secret_key = 'xyz'

#config the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app) #initalize db
with app.app_context():
  db.create_all()
  db.session.commit()

# import declared routes
import routes


if __name__ == "__main__":
    app.run(debug=True)