import time

from flask import render_template, redirect, url_for, session, request

from app import app
from app.models import db, User, Dish, Category, Order
from app.forms import RegisterForm, OrderForm, AuthFrom

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


def get_username_from_session():
    username = ''
    user = session.get('user')
    if user:
        username = user['username']
    return username

@app.route('/')
def render_main():
    categories = db.session.query(Category).all()
    dishes = db.session.query(Dish).all()
    cart_text = get_cart_text()
    username = get_username_from_session()
    return render_template('main.html', categories=categories, dishes=dishes, cart_text=cart_text, username=username)


@app.route('/register', methods=['GET', 'POST'])
def render_register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    elif request.method == 'POST':
        mail = form.mail.data
        username = form.username.data
        password = form.password.data
        password2 = form.password2.data

        if not form.validate():
            return render_template('register.html', form=form)

        error_messages = []
        if password != password2:
            error_messages.append('Пароли не совпадают!')

        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            error_messages.append('Пользователь с таким username уже существует!')

        existing_mail = User.query.filter_by(mail=mail).first()
        if existing_mail:
            error_messages.append('Пользователь с такой электропочтой уже существует!')

        if error_messages:
            return render_template('register.html', form=form, error_msg=' '.join(error_messages))

        user = User(mail=mail,
                    username=username,
                    password=password,
                    role='user')
        db.session.add(user)
        db.session.commit()
        return render_template('register_success.html', username=username)


@app.route('/auth', methods=['GET', 'POST'])
def render_auth():
    form = AuthFrom()
    if request.method == 'POST':
        user = User.query.filter_by(mail=form.mail.data).first()

        if user and user.password_valid(form.password.data):
            session["user"] = {
                "id": user.id,
                "username": user.username,
                "role": user.role,
            }
            return redirect("/")
        else:
            return render_template('auth.html', form=form, error_msg='Неверное имя пользователя или пароль')
    return render_template('auth.html', form=form)


@app.route('/logout')
def render_logout():
    session.pop('user')
    return redirect(url_for('render_auth'))


@app.route('/account')
def render_account():
    username = get_username_from_session()
    return render_template('account.html', username=username)


@app.route('/cart')
def render_cart():
    username = get_username_from_session()
    print(username)
    is_auth = bool(session.get('user'))
    if not is_auth:
        return redirect(url_for('render_auth'))

    dish_ids = session.get(SESSION_KEY_OF_CART, [])
    dishes = []
    summ = 0
    for dish_id in dish_ids:
        dish = db.session.query(Dish).get(dish_id)
        dishes.append(dish)
        summ += dish.price
    form = OrderForm(order_summ=summ, order_cart=dish_ids)
    return render_template('cart.html', dishes=dishes, form=form, decline_dish=decline_dish, username=username)


@app.route('/ordered', methods=['POST'])
def render_ordered():
    form = OrderForm()
    name = form.name.data
    address = form.address.data
    email = form.email.data
    phone = form.phone.data
    order_summ = form.order_summ.data
    dish_list = form.order_cart.data
    order = Order(date=time.time(),
                  order_price=order_summ,
                  status='NEW',
                  phone=phone,
                  address=address,
                  dish_list=dish_list,
                  owner=db.session.query(User).get())
    return render_template('ordered.html')


@app.route('/add_to_cart/<int:dish_id>')
def add_to_cart(dish_id):
    dishes = session.get(SESSION_KEY_OF_CART, [])
    dishes.append(dish_id)
    session[SESSION_KEY_OF_CART] = dishes
    return redirect(url_for('render_main'))


@app.route('/delete_from_cart/<int:dish_id>')
def delete_from_cart(dish_id):
    dishes = session.get(SESSION_KEY_OF_CART, [])
    dishes.remove(dish_id)
    session[SESSION_KEY_OF_CART] = dishes
    return redirect(url_for('render_cart'))
