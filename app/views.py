from flask import render_template, redirect, url_for, session

from app import app
from app.models import db, User, Dish, Category


@app.route('/')
def render_main():
    categories = db.session.query(Category).all()
    dishes = db.session.query(Dish).all()
    dishes_in_cart = session.get('dishes', [])
    sum = 0
    for dish_in_cart in dishes_in_cart:
        dish_in_cart_entity = db.session.query(Dish).get(dish_in_cart)
        sum += dish_in_cart_entity.price

    return render_template('main.html', categories=categories, dishes=dishes, dishes_in_cart=dishes_in_cart, sum=sum)


@app.route('/register')
def render_register():
    return render_template('register.html')


@app.route('/auth')
def render_auth():
    return render_template('auth.html')


@app.route('/account')
def render_account():
    return render_template('account.html')


@app.route('/cart')
def render_cart():
    return render_template('cart.html')


@app.route('/ordered')
def render_ordered():
    return render_template('ordered.html')


@app.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    dishes = session.get('dishes', [])
    dishes.append(dish_id)
    session['dishes'] = dishes
    return redirect(url_for('render_main'))
