from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from toodoo import db
from .forms import LoginForm, RegisterForm, DeleteForm
from .models import Users, generate_password_hash, check_password_hash

# Creates the main blueprint that gets sent to init
main_bp = Blueprint('main', __name__)


""" LOGIN ROUTES """
@main_bp.route('/', methods=["GET", "POST"])
def index():
    form = LoginForm()

    # POST request
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        # Validating email
        if not user:
            flash('Incorrect Email!')
            return redirect(url_for('main.index'))
        
        # Validating password
        if not check_password_hash(user.password_hash, form.password.data):
            flash('Incorrect password!')
            return redirect(url_for('main.index'))
        
        login_user(user)
        return redirect(url_for('main.user_dashboard'))
    
    # GET request
    return render_template('auth/login.html', form=form)


@main_bp.route('/user/add', methods=["GET", "POST"])
def add_user():
    form = RegisterForm()
    # POST request
    if form.validate_on_submit():
        
        user = Users.query.filter_by(email=form.email.data).first()
        if user == None:
            # Hashing pass
            hashed_pw = generate_password_hash(form.password.data)

            # Adding to db if no users exists
            user = Users(first_name=form.first_name.data,
                         last_name=form.last_name.data, 
                         email=form.email.data,
                         password_hash=hashed_pw)
            
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


""" ERROR ROUTES """
# Moved inside factory function


""" ADMIN ROUTES """
@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin/admin_dashboard.html')

# Admin - Dashboard
@main_bp.route('/admin/users')
@login_required
def admin_users():
    users = Users.query.order_by(Users.date_added)
    form = DeleteForm()
    return render_template('admin/users.html', users=users, form=form)


# Admin - User Delete
@main_bp.route('/users/delete/<int:id>', methods=["POST"])
@login_required
def delete_user(id):        
    user = Users.query.filter_by(id=id).first()

    if not user:
        flash('No user found!')
    else:
        try:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!')
        except Exception as e:
            db.session.rollback()
            flash(f'User deletion failed: {str(e)}')

    #TODO: Add logic to check user role and route accordingly
    return redirect(url_for('main.index'))


""" USER MANAGEMENT """
# Dashboard
@main_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    return render_template('users/user_dashboard.html')

# Logout
@main_bp.route('/user/logout')
@login_required
def user_logout():
    logout_user()
    flash('Logged out Successfully!')
    return redirect(url_for('main.index'))


#TODO: Edit User Route