from flask import Blueprint, render_template, redirect, url_for, flash
from toodoo import db
from .forms import LoginForm, RegisterForm
from .models import Users

# Creates the main blueprint that gets sent to init
main_bp = Blueprint('main', __name__)


""" LOGIN ROUTES """
@main_bp.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()

    # POST request
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    
    # GET request
    return render_template('auth/login.html', form=form)


@main_bp.route('/add_user', methods=["GET", "POST"])
def add_user():
    form = RegisterForm()

    # POST request
    if form.validate_on_submit():
        
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user == None:
            # Adding to db if no users exists
            user = Users(name=form.name.data, 
                         email=form.email.data,
                         password_hash=form.password.data)
            
            # Commit to db
            db.session.add(user)
            db.session.commit()
            
            # Flash and redirect
            flash('User added successfully!')
            return redirect(url_for('main.index'))
        
        else:
            flash('User already registered!')
            return redirect(url_for('main.index'))
    
    # GET request
    return render_template('auth/register.html', form=form)


""" ADMIN ROUTES """
@main_bp.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

@main_bp.route('/admin/users')
def admin_users():
    users = Users.query.order_by(Users.date_added)
    return render_template('admin/users.html', users=users)