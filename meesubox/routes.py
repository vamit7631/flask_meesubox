from meesubox import app
from flask import render_template, redirect, url_for, flash
from meesubox.models import UserModel
from meesubox.forms import RegisterForm , LoginForm
from meesubox import db

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user_record = UserModel(firstname = form.firstname.data, lastname = form.lastname.data, mobile_no = form.mobile_no.data, email_id = form.email_id.data, password = form.password.data )
        try:
            db.session.add(new_user_record)
            db.session.commit()
            return redirect('/')
        except:
            print('There was an error with creating a user')   
    else:
        return render_template('signup.html', form=form)    




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        user_check = UserModel.query.filter_by(email_id = form.email_id.data).first()
        if user_check and user_check.check_password_correction(
            attempted_password = form.password.data
        ):    
            login_user(user_check)
            flash(f'Success! You are logged in as: {user_check.email_id}', category='success')
            return redirect(url_for('/'))
        else:
            flash('email and password are not match! Please try again', category='danger')
    return render_template('signin.html', form=form)