from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'


db=SQLAlchemy(app)
bycrypt=Bcrypt()
bycrypt.init_app(app)
login_manager=LoginManager()
login_manager.init_app(app)

from market import routes