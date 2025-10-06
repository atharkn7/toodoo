from flask import Flask
from .routes import main_bp


# app config
app = Flask(__name__)
# App Configurations
app.config['SECRET_KEY'] = 'pass'   # Secret Key

# Gets all routes from main_bp
app.register_blueprint(main_bp)