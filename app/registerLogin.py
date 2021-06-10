from flask import Flask, render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db, login

app = Flask (__name__)
app.secret_key = 'xyz'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app (app)
login.init_app (app)
login.login_view = 'login'


@app.before_first_request
def create_all():
    db.create_all ( )


@app.route ('/index')
@login_required
def index():
    return render_template ('index.html')


@app.route ('/login', methods=['POST', 'GET'])
def login():
    msg=''
    if current_user.is_authenticated:
        return redirect ('/index')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user=UserModel(username=username, password=password )
        user = user.check_username_exist(username)
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect('/index')
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route ('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect ('/index')

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user=UserModel(firstname=firstname, lastname=lastname,email=email, username=username)
        if user.check_username_exist(username):
            msg = 'Username is already exist'
            return render_template('register.html', msg=msg)

        if user.check_email_exist(email):
            msg = 'Email is already exist'
            return render_template('register.html', msg=msg)

        user.set_password(password)
        if user.add_user(user, app):
            return redirect ('/login')
    return render_template ('register.html')

@app.route ('/logout')
def logout():
    logout_user ( )
    return redirect ('/index')
