from meesubox import app
from flask import render_template
from meesubox.models import UserModel

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')