from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Stay logged in?")
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Stay logged in?")
    submit = SubmitField("Register")
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise VaildationError('Email already in use')

class ProfileForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    save = SubmitField("Save Changes")
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise VaildationError('Email already in use')
