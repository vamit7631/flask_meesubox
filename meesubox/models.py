from meesubox import db
from datetime import datetime

class UserModel(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(length=30), nullable=False)
    lastname = db.Column(db.String(length=30), nullable=False)
    mobile_no = db.Column(db.String(length=12), nullable=False, unique=True)
    email_id  = db.Column(db.String(length=200), nullable=False, unique=True)
    password = db.Column(db.String(length=200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'UserModel {self.firstname}'