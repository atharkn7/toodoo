from flask import Blueprint, render_template


# Creates the main blueprint that gets sent to init
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('home.html')