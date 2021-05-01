from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, Optional
from meesubox.models import UserModel, ProductItem

class RegisterForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[Length(min=2, max=30), DataRequired()])
    lastname = StringField(label='Last Name', validators=[Length(min=2, max=30), DataRequired()])
    mobile_no = StringField(label='Mobile No', validators=[Length(min=10, max=10), DataRequired()])
    email_id = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    email_id = StringField(label='Email Address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Login')   


class AddProductDetails(FlaskForm):
    product_name = StringField(label='Product name', validators=[DataRequired()]) 
    product_price = StringField(label='Product price', validators=[DataRequired()]) 
    product_category = StringField(label='Product category', validators=[DataRequired()])
    product_size = StringField(label='Product size', validators=[DataRequired()])
    product_description = TextAreaField(label='Product description', validators=[DataRequired()])
    quantity = IntegerField(label='Quantity', validators=[DataRequired()])
    product_discount = StringField(label='Product discount', validators=[DataRequired()]) 
    # sku_id 
    # store_id
    store_name = StringField(label='Store name', validators=[DataRequired()]) 
    new_product = BooleanField(validators=[Optional()], render_kw={'checked': False}) 
    # featured_product
    best_seller = BooleanField(validators=[Optional()], render_kw={'checked': False})  
    submit = SubmitField(label='Submit')    



class AddCategoryDetails(FlaskForm):
        category_name = StringField(label='Category name', validators=[DataRequired()]) 
        category_slug = StringField(label='Category slug', validators=[DataRequired()]) 
        parent_category = IntegerField(label='Parent Category', validators=[Optional()])
        assign_parent_category = BooleanField(validators=[Optional()], render_kw={'checked': False})  
        submit = SubmitField(label='Submit') 


