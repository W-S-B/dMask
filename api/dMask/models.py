from datetime import datetime
from dMask import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    secret = db.Column(db.String(60), nullable=True)

    def __repr__(self):
        return f"User('{self.username}')"


class Status(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    masks_count = db.Column(db.Integer, nullable=False)
    passed_people = db.Column(db.Integer, nullable=False)  # Total
    passed_green = db.Column(db.Integer, nullable=False)  # People who wear а mask correctly
    passed_yellow = db.Column(db.Integer, nullable=False)  # People who wear а mask INcorrectly
    passed_red = db.Column(db.Integer, nullable=False)  # People who do NOT wear a mask

    def __repr__(self):
        return f"Daily status('{self.masks_count}', '{self.passed_people}')"
