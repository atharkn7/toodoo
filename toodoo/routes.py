from flask import Blueprint, render_template, redirect, url_for, flash, request
from toodoo import db
from .forms import LoginForm, RegisterForm, DeleteForm
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


@main_bp.route('/user/add', methods=["GET", "POST"])
def add_user():
    form = RegisterForm()

    # POST request
    if form.validate_on_submit():
        
        user = Users.query.filter_by(email=form.email.data).first()
        
        if user == None:
            # Adding to db if no users exists
            user = Users(first_name=form.first_name.data,
                         last_name=form.last_name.data, 
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
    form = DeleteForm()
    return render_template('admin/users.html', users=users, form=form)


""" USER MANAGEMENT """
@main_bp.route('/users/delete/<int:id>', methods=["POST"])
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