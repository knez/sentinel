from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    notify = db.Column(db.Boolean)

class Video(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    kind = db.Column(db.String(25))
    position = db.Column(db.String(25))
    filename = db.Column(db.String(100))
