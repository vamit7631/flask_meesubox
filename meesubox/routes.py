from meesubox import app
from flask import render_template, redirect, url_for
from meesubox.models import UserModel
from meesubox.forms import RegisterForm
from meesubox import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form, "-----------------------------Amit")
        new_user_record = UserModel(firstname = form.firstname.data, lastname = form.lastname.data, mobile_no = form.mobile_no.data, email_id = form.email_id.data, password = form.password.data )
        db.session.add(new_user_record)
        db.session.commit()
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            print(f'There was an error with creating a user: {err_msg}')    
    return render_template('signup.html', form=form)    