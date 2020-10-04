from flask_sqlalchemy import SQLAlchemy

# from werkzeug.security import generate_password_hash, check_password_hash

# Настройки соединения сделаем позже в модуле приложения
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    orders = db.relationship("Order")


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    category = db.relationship("Category")
    owner_id = db.Column(db.Integer, db.ForeignKey("categories.id"))


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dishes = db.relationship("Dish")


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    order_price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    owner = db.relationship("User")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
