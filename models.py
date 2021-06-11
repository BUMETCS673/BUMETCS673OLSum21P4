from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from app import db

db = SQLAlchemy()


class MealModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  meal_type = db.Column(db.String(200), nullable=False)
  food_item1 = db.Column(db.String(200), nullable=False)
  food_item2 = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow) 

  def __repr__(self):
    return '<Task %r>' % self.id

