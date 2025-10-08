import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()   # create db object but don’t bind yet
migrate = Migrate() # create migrate
login_manager = LoginManager()


def create_app():
    """
    Application factory function.
    Creates and configures the Flask app instance,
    initializes the database and migration extensions,
    and registers blueprints.s
    """
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toodoo.db'

    # Initialize extensions *after* app is created
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.index'

    # Import models here to avoid circular imports
    from .models import Users

    # Loading users from Users model
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))


    # Import blueprints after db is ready
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app