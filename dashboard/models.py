from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    notify = db.Column(db.Boolean)
