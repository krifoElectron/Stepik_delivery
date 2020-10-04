from flask import render_template, redirect, url_for, session

from app import app
from app.models import db, User, Dish, Category

SESSION_KEY_OF_CART = 'cart'


def get_cart_text():
    dishes_in_cart = session.get(SESSION_KEY_OF_CART, [])
    number_of_dishes = len(dishes_in_cart)
    if not number_of_dishes:
        return 'Корзина пуста'
    sum = 0
    for dish_in_cart in dishes_in_cart:
        dish_in_cart_entity = db.session.query(Dish).get(dish_in_cart)
        sum += dish_in_cart_entity.price
    return f'В корзине {number_of_dishes} {decline_dish(number_of_dishes)} на сумму {sum} руб'


def decline_dish(dish_number):
    remainder = dish_number % 10
    if remainder == 0 or remainder >= 5 or (10 <= dish_number <= 19):
        return 'блюд'
    elif remainder == 1:
        return 'блюдо'
    else:
        return 'блюда'


@app.route('/')
def render_main():
    categories = db.session.query(Category).all()
    dishes = db.session.query(Dish).all()
    cart_text = get_cart_text()
    return render_template('main.html', categories=categories, dishes=dishes, cart_text=cart_text)


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
    dishes = session.get(SESSION_KEY_OF_CART, [])
    dishes.append(dish_id)
    session[SESSION_KEY_OF_CART] = dishes
    return redirect(url_for('render_main'))
