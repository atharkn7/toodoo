from flask import Flask
from .routes import main_bp


# app config
app = Flask(__name__)

# Gets all routes from main_bp
app.register_blueprint(main_bp)