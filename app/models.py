from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from sqlalchemy import exc
from datetime import datetime

login = LoginManager()
db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(20))
    role = db.Column(db.String(20))

    def __init__(self, firstname='', lastname='', email='', username='', password='', role=''):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        return self.password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_username_exist(self, username):
        return UserModel.query.filter_by(username=username).first()

    def check_email_exist(self, email):
        return UserModel.query.filter_by(email=email).first()

    def add_user(self, user):
        try:
            db.session.add(user)
            db.session.flush()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            return True

    def check_admin(self, username):
        if UserModel.query.filter_by(username=username, role='admin').first():
            return True
        else:
            return False

class MealModel(db.Model):
  __bind_key__ = 'two'
  __tablename__ = 'meals'

  id = db.Column(db.Integer, primary_key=True)
  meal_type = db.Column(db.String(200), nullable=False)
  food_item1 = db.Column(db.String(200), nullable=False)
  food_item2 = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.utcnow)


@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))


class Admin(UserModel):

    def retrieve_user(self, username):
        user = UserModel.query.filter_by(username=username).first()
        return user

    def delete_user(self, id):
        user = UserModel.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.flush()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            return True

    def add_admin_user(self, firstname, lastname, email, username, password):
        admin_user = Admin(firstname, lastname, email,
                           username, password, 'admin')
        admin_user.password = admin_user.set_password(admin_user.password)
        try:
            db.session.add(admin_user)
            db.session.flush()
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            return True

