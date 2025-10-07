from flask import Blueprint, render_template, redirect, url_for
from .forms import LoginForm, RegisterForm


# Creates the main blueprint that gets sent to init
main_bp = Blueprint('main', __name__)


""" LOGIN ROUTES """
@main_bp.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html', form=form)


@main_bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', form=form)