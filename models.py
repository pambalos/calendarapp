from main import db, login_manager #importing db and login manager from main.py app
from flask import request
from flask_login import UserMixin #additional setup required for using login_manager
from datetime import datetime #used for checking time
from keys import *

import requests

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)

class CbookInfo(db.Model):
    userID = db.Column(db.Integer)
    access_code = db.Column(db.String(60))
    refresh_token = db.Column(db.String(60))
    token_expires = db.Column(db.DateTime)

    def update(self, access_code, refresh_token, token_expires):
        self.access_code = access_code
        self.refresh_token = refresh_token
        self.token_expires = token_expires
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    first_name = db.Column(db.String(20), unique = False)
    last_name = db.Column(db.String(20), unique = False)

    def update(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        db.session.commit()

    def __repr__(self):
        return f"User('{ self.email }', '{ self.id }')"
