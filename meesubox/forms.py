from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class RegisterForm(FlaskForm):
    firstname = StringField(label='First Name')
    lastname = StringField(label='Last Name')
    mobile_no = StringField(label='Mobile No')
    email_id = StringField(label='Email Address')
    password = PasswordField(label='Password')
    submit = SubmitField(label='Sign Up')