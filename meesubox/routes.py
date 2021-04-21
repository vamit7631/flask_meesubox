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
        new_user_record = UserModel(firstname = form.firstname.data, lastname = form.lastname.data, mobile_no = form.mobile_no.data, email_id = form.email_id.data, password = form.password.data )
        try:
            db.session.add(new_user_record)
            db.session.commit()
            return redirect('/')
        except:
            print('There was an error with creating a user')   
    else:
        return render_template('signup.html', form=form)    