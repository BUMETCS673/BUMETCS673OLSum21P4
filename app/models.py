from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager

login = LoginManager ( )
db = SQLAlchemy ( )


class UserModel (UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String (80), unique=True)
    username = db.Column(db.String (100), unique=True)
    password = db.Column(db.String ( ))

    def set_password(self, password):
        self.password = generate_password_hash(password);

    def check_password(self, password):
        return check_password_hash(self.password, password);


@login.user_loader
def load_user(id):
    return UserModel.query.get (int (id))