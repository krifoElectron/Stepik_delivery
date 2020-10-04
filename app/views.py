from flask import render_template

from app import app
from app.models import db, User, Dish, Category


@app.route('/')
def render_main():
    categories = db.session.query(Category).all()
    dishes = db.session.query(Dish).all()
    return render_template('main.html', categories=categories, dishes=dishes)


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


@app.route('/add_to_cart')
def add_to_cart():
    return 'add'
