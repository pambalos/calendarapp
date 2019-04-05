from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from flask_oauthlib.client import OAuth
from keys import *
from forms import *
from models import *

app = Flask(__name__, static_folder = './public', template_folder = './static')
app.config['SECRET_KEY'] = "sZWjFJmyFQnzkVMxbOIAIZNJhaJV"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #importing sqldatabase

db = SQLAlchemy(app)
db.app = app
oauth = OAuth(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from templates.calendar.views import calendar_blueprint
from templates.profile.views import profile_blueprint


app.register_blueprint(profile_blueprint)
app.register_blueprint(calendar_blueprint)
