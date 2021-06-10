from flask import Flask, render_template, request, redirect, flash
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db, login, Admin

app = Flask(__name__)
app.secret_key = 'xf7\xc4\xfa\x91'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'

user = UserModel()
admin = Admin()


@app.before_first_request
def create_all():
    db.create_all()
    admin.add_admin_user('John', 'Boyle', 'admin1@123.com', 'admin1', 'admin1')
    admin.add_admin_user('Stephen', 'Best', 'admin2@123.com', 'admin2', 'admin2')


@app.route('/index')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if current_user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            if user.role == 'customer':
                user = UserModel(user.firstname, user.lastname, user.email,
                                user.username, user.password, user.role)

                path = '/index'
            else:
                user = Admin(user.firstname, user.lastname, user.email,
                             user.username, user.password, user.role)
                path = '/admin/data'
            user = user.check_username_exist(username)
            if user.check_password(password):
                login_user(user)
                return redirect(path)
            else:
                msg = 'Incorrect password!'
        else:
            msg = 'Incorrect username!'

    return render_template('login.html', msg=msg)


@app.route('/register', methods=['POST', 'GET'])
def register():
    msg = ' '
    role = 'customer'
    if current_user.is_authenticated:
        return redirect('/index')

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        customer = UserModel(firstname, lastname, email,
                            username, password, role)
        if customer.check_username_exist(username):
            msg = 'Username is already exist'
            return render_template('register.html', msg=msg)

        if customer.check_email_exist(email):
            msg = 'Email is already exist'
            return render_template('register.html', msg=msg)

        customer.set_password(password)
        if customer.add_user(customer):
            msg = 'User is added successfully!'
            return redirect('/login')
        else:
            msg = 'Failed to add the user!'
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route('/admin/data/', methods=['GET', 'POST'])
@login_required
def get_user_data():
    if request.method == 'GET':
        return render_template('userinput.html')

    if request.method == 'POST':
        username = request.form['username']
        return redirect(f'/admin/data/{username}')


@app.route('/admin/data/<string:username>', methods=['GET', 'POST'])
@login_required
def display_user_detail(username):
    user1 = (Admin(user)).retrieve_user(username)
    if user1:
        return render_template('userlist.html', user=user1)
    else:
        return redirect(f'/admin/data/')


@app.route('/admin/data/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_record(id):
    user = UserModel.query.get_or_404(id)
    if request.method == 'POST':
        user.firstname = request.form['firstname']
        user.lastname = request.form['lastname']
        user.username = request.form['username']
        user.password = request.form['password']
        user.password = user.set_password(user.password)
        user.email = request.form['email']

        try:
            db.session.commit()
            return redirect(f'/admin/data/{user.username}')
        except:
            return "Problem to updating the user record."
    else:
        return render_template('userupdate.html', user=user)


@app.route('/admin/data/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user_record(id):
    if (Admin(user)).delete_user(id):
        return redirect('/admin/data')
    else:
        return "Problem to deleting the user record."


