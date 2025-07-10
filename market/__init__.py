# market/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = 'auth.login_page'
login_manager.login_message_category = 'info'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Import inside function to avoid circular import
    from market.auth import auth_bp
    from market.blog import blog_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)

    return app
