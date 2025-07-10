from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'


db=SQLAlchemy(app)
bcrypt=Bcrypt()
bcrypt.init_app(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'  # Redirect to login_page if user is not authenticated
login_manager.login_message_category = 'info'  # Flash message category for login required

from market import routes