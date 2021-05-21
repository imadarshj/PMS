from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    phone = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    reports = db.relationship('Report', backref='patient', lazy=True)

    def __repr__(self):
        return f"Üser('{self.username}', '{self.email}', '{self.image_file}')"

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(100), nullable=False)
    sex = db.Column(db.String(100), nullable=False)
    cp = db.Column(db.String(100), nullable=False)
    trestbps = db.Column(db.String(100), nullable=False)
    chol = db.Column(db.String(100), nullable=False)
    fbs = db.Column(db.String(100), nullable=False)
    restecg = db.Column(db.String(100), nullable=False)
    thalach = db.Column(db.String(100), nullable=False)
    exang = db.Column(db.String(100), nullable=False)
    oldpeak = db.Column(db.String(100), nullable=False)
    slope = db.Column(db.String(100), nullable=False)
    ca = db.Column(db.String(100), nullable=False)
    thal = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)