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
        self.password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8);

    def check_password(self, password):
        return check_password_hash(self.password, password);

    def check_username_exist(self, username):
        return UserModel.query.filter_by(username=username).first()

    def check_email_exist(self, email):
        return UserModel.query.filter_by(email=email).first()

    def add_user(self, user, app):
        try:
            db.session.add(user)
            db.session.flush()
        except exceptions.SQLAlchemyError:
            db.session.rollback()
            app.logger.error("DB rollback for user - ", user.username)
            return False
        else:
            db.session.commit()
            app.logger.info('User is added successfully! - ', user.username)
            return True

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))