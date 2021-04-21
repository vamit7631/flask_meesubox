from meesubox import app
from flask import render_template, redirect, url_for, flash
from meesubox.models import UserModel
from meesubox.forms import RegisterForm , LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from meesubox import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/index')
@login_required
def index():
    # print(current_user.firstname,"-------------------------test")
    return render_template('index.html', name=current_user.firstname)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user_record = UserModel(firstname = form.firstname.data, lastname = form.lastname.data, mobile_no = form.mobile_no.data, email_id = form.email_id.data, password = generate_password_hash(form.password.data, method='sha256') )
        try:
            db.session.add(new_user_record)
            db.session.commit()
            return redirect(url_for('signin'))
        except:
            print('There was an error with creating a user')   
    else:
        return render_template('signup.html', form=form)    




@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = UserModel.query.filter_by(email_id = form.email_id.data).first()
            if not user or not check_password_hash(user.password, form.password.data):   
                return redirect(url_for('signin'))
        
            login_user(user, remember=True)
            return redirect(url_for('index'))
        return render_template('signin.html', form=form)
    
    else:
        return redirect(url_for('index'))


@app.route('/signout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for("home_page"))
  