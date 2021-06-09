
from app import app, db
from models import MealModel
from flask import json, render_template, url_for, jsonify, request, redirect
#route for Home Page
@app.route("/")  #home page route
def home():
    return render_template('index.html')

#route for About page
@app.route("/about") #render about page
def about():
    return render_template('about.html')

#route to CREATE a meal entry
@app.route('/foodinput', methods=['POST', 'GET']) #render food input page
def foodinput():
    #get the data from the form
    if request.method == 'POST':
        # print("REQUEST", request.data)
        meal_type = request.form['meal_type']
        food_item1 = request.form['fitem1']
        food_item2 = request.form['fitem2']

        #use the received data to instantiate a Meal object
        new_meal = MealModel(meal_type=meal_type, food_item1=food_item1, food_item2=food_item2)

        #push the data to the sqlite db
        try:
            db.session.add(new_meal)
            db.session.commit()
            return render_template('foodinput.html', message="Meal Added")

        except:
          return render_template('foodinput.html', message="There was an issue adding your meal details")

    else:
      meals = MealModel.query.order_by(MealModel.date_created).all()
      return render_template('foodinput.html', message="")

@app.route('/foodtable', methods=['GET']) #render food table page
def foodtable():
  #get the data from the form
  try:
    meals = MealModel.query.order_by(MealModel.date_created).all()
    return render_template('foodtable.html', meals=meals)
  except:
    return "There was an issue displaying your meals"

#route to DELETE a meal entry
@app.route('/delete/<int:id>')
def delete_meal(id):
  delete_meal = MealModel.query.get_or_404(id)
    
  try:
    db.session.delete(delete_meal)
    db.session.commit()
    return redirect('/foodtable')
  
  except:
    return "There was an issue deleting your meal"

#route to UPDATE a meal entry
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_meal(id):
  meal = MealModel.query.get_or_404(id)
  
  if request.method == 'POST':
    meal.meal_type = request.form['meal_type']
    meal.food_item1 = request.form['fitem1']
    meal.food_item2 = request.form['fitem2']

    try:
      db.session.commit()
      return redirect('/foodtable')
  
    except:
      return "There was an issue updating your meal"

  else:
    return render_template('update.html', meal=meal)
  
