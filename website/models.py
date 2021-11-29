from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    collections = db.relationship('Collection')



class Collection(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    date = db.Column (db.DateTime(timezone=True), default= func.now())
    name = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cards = db.relationship('Card')



class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(1500))
    answer = db.Column(db.String(1500))
    date = db.Column (db.DateTime(timezone=True), default= func.now())
    collection_id  = db.Column(db.Integer, db.ForeignKey('collection.id'))

