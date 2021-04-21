from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meesubox.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d546gfgvbd'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "signin"
login_manager.init_app(app)
# login_manager.login_message_category = "info"
from meesubox import routes
