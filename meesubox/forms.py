from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired

class RegisterForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='Last Name', validators=[Length(min=2, max=30), DataRequired()])
    mobile_no = StringField(label='Mobile No', validators=[Length(min=10, max=10), DataRequired()])
    email_id = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Sign Up')