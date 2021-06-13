from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user
from models import UserModel, db, login, Admin
from sqlalchemy import exc
from app import *
from usda import extract_avg_calorie_data, usda_api_call, load_cfg

# db.init_app(app)
login.init_app(app)
login.login_view = 'login'


# route for Home Page
@app.route("/")  # home page route
def home():
    return render_template('index.html')


# route for About page
@app.route('/about')  # render about page
def about():
    return render_template('about.html')


@app.route('/foodinput')
@login_required
def user_dashboard():
    return render_template('foodinput.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ''
    if current_user.is_authenticated:
        return redirect('/foodinput')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserModel.query.filter_by(username=username).first()
        if user is not None:
            if user.role == 'customer':
                user = UserModel(user.firstname, user.lastname, user.email, user.username, user.password, user.role)

                path = '/foodinput'
            else:
                user = Admin(user.firstname, user.lastname, user.email, user.username, user.password, user.role)
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

        customer = UserModel(firstname, lastname, email, username, password, role)
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
    return render_template('register.html', msg=msg)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/admin/data', methods=['GET', 'POST'])
@login_required
def get_user_data():
    if user.check_admin(current_user.username):
        if request.method == 'GET':
            return render_template('userinput.html')

        if request.method == 'POST':
            username = request.form['username']
            return redirect(f'/admin/data/{username}')
    else:
        return redirect('/')


@app.route('/admin/data/<string:username>', methods=['GET', 'POST'])
@login_required
def display_user_detail(username):
    if user.check_admin(current_user.username):
        user1 = (Admin(user)).retrieve_user(username)
        if user1:
            return render_template('userlist.html', user=user1)
        else:
            return redirect(f'/admin/data')
    else:
        return redirect('/')


@app.route('/admin/data/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user_record(id):
    if user.check_admin(current_user.username):
        user1 = UserModel.query.get_or_404(id)
        if request.method == 'POST':
            user1.firstname = request.form['firstname']
            user1.lastname = request.form['lastname']
            user1.username = request.form['username']
            user1.password = request.form['password']
            user1.password = user.set_password(user1.password)
            user1.email = request.form['email']
            try:
                db.session.commit()
                return redirect(f'/admin/data/{user1.username}')
            except exc.SQLAlchemyError:
                return "Problem to updating the user record."
        else:
            return render_template('userupdate.html', user=user1)
    else:
        redirect('/')


@app.route('/admin/data/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user_record(id):
    if user.check_admin(current_user.username):
        if (Admin(user)).delete_user(id):
            return redirect('/admin/data')
        else:
            return "Problem to deleting the user record."
    else:
        redirect('/')


# route to CREATE a meal entry
@app.route('/foodinput', methods=['POST', 'GET'])  # render food input page
#@login_required
def foodinput():
    # get the data from the form
    if request.method == 'POST':
        # print("REQUEST", request.data)
        meal_type = request.form['meal_type']
        food_item1 = request.form['fitem1']
        food_item2 = request.form['fitem2']

        try:
            calorie1 = extract_avg_calorie_data(usda_api_call(food_item1, load_cfg()))
        except Exception as e:
            return render_template('foodinput.html', message=e)

        try:
            calorie2 = extract_avg_calorie_data(usda_api_call(food_item2, load_cfg()))
        except Exception as e:
            return render_template('foodinput.html', message=e)

        calorie_total = calorie1 + calorie2
        print(calorie_total)
        # use the received data to instantiate a Meal object
        new_meal = MealModel(meal_type=meal_type, food_item1=food_item1, food_item2=food_item2, calories=calorie_total)

        # push the data to the sqlite db
        try:
            db.session.add(new_meal)
            db.session.commit()
            return render_template('foodinput.html', message="Meal Added")

        except:
            return render_template('foodinput.html', message="There was an issue adding your meal details")

    else:
        meals = MealModel.query.order_by(MealModel.date_created).all()
        return render_template('foodinput.html', message="")


@app.route('/foodtable', methods=['GET'])  # render food table page
@login_required
def foodtable():
    # get the data from the form
    try:
        meals = MealModel.query.order_by(MealModel.date_created).all()
        return render_template('foodtable.html', meals=meals)
    except:
        return "There was an issue displaying your meals"


# route to DELETE a meal entry
@app.route('/delete/<int:id>')
@login_required
def delete_meal(id):
    delete_meal = MealModel.query.get_or_404(id)

    try:
        db.session.delete(delete_meal)
        db.session.commit()
        return redirect('/foodtable')

    except:
        return "There was an issue deleting your meal"


# route to UPDATE a meal entry
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_meal(id):
    meal = MealModel.query.get_or_404(id)

    if request.method == 'POST':
        meal.meal_type = request.form['meal_type']
        meal.food_item1 = request.form['fitem1']
        meal.food_item2 = request.form['fitem2']

        try:
            calorie1 = extract_avg_calorie_data(usda_api_call(meal.food_item1, load_cfg()))
            print("Inside food_item1 api calorie call")
        except Exception as e:
            return render_template('foodtable.html', message=e)

        try:
            calorie2 = extract_avg_calorie_data(usda_api_call(meal.food_item2, load_cfg()))
            print("Inside food_item2 api calorie call")
        except Exception as e:
            return render_template('foodtable.html', message=e)

        meal.calories = calorie1 + calorie2
        print(meal.calories)
        try:
            db.session.commit()
            return redirect('/foodtable')

        except:
            return "There was an issue updating your meal"

    else:
        return render_template('update.html', meal=meal)
