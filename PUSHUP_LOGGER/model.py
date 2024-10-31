from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(200), nullable=False)
    email=db.Column(db.String(200), unique=True,nullable=False)
    password=db.Column(db.String(200), nullable=False)
    workouts=db.relationship('Workout', backref='author', lazy=True)

class Workout(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    pushups=db.Column(db.Integer, nullable=False)
    date_posted=db.Column(db.DateTime, default=datetime.utcnow)
    comment=db.Column(db.String(500), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False )
