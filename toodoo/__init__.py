import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()   # create db object but don’t bind yet
# migrate = Migrate()

def create_app():
    """
    Application factory function.
    Creates and configures the Flask app instance,
    initializes the database and migration extensions,
    and registers blueprints.s
    """
    app = Flask(__name__)

    # Make sure instance folder exists
    # os.makedirs(app.instance_path, exist_ok=True)

    # Configure app
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toodoo.db'

    # Initialize db *after* app is created
    db.init_app(app)

    # Import blueprints after db is ready
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app