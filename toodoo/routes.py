from datetime import date, time
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from toodoo import db
from .forms import LoginForm, RegisterForm, DeleteForm, EditUser, UpdateUserPass, CreateTask
from .models import Users, Tasks, generate_password_hash, check_password_hash

# Creates the main blueprint that gets sent to init
main_bp = Blueprint('main', __name__)


""" LOGIN ROUTES """
# Index handles Login
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



""" ADMIN ROUTES """
@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    tasks = Tasks.query.all()
    return render_template('admin/admin_dashboard.html', tasks=tasks)

# Admin - Dashboard
@main_bp.route('/admin/users')
@login_required
def admin_manage_users():
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
# Login landing route
@main_bp.route('/user')
@login_required
def user_home_redirect():
    # Does not do anything as of now
    return redirect(url_for('main.user_dashboard'))

# Dashboard
@main_bp.route('/user/dashboard')
@login_required
def user_dashboard():
    #TODO: Show only due and today's tasks
    return redirect(url_for('main.task_list'))

# Logout
@main_bp.route('/user/logout')
@login_required
def user_logout():
    logout_user()
    flash('Logged out Successfully!')
    return redirect(url_for('main.index'))

#TODO: Profile View Route
@main_bp.route('/user/profile')
@login_required
def user_profile():
    return render_template('/users/user_profile.html')

@main_bp.route('/user/edit/<int:id>', methods=["GET", "POST"])
@login_required
def user_edit(id):
    # Forms
    edit_form = EditUser()   # Reusing register here
    delete_form = DeleteForm()

    user_to_update = Users.query.get_or_404(id)

    if not current_user.id == id:   # Add admin logic
        flash('Unauthorized access!')
        return redirect('main.user_dashboard')
    

    if edit_form.validate_on_submit():
        # Updating values of user
        user_to_update.first_name = edit_form.first_name.data
        user_to_update.last_name = edit_form.last_name.data
        user_to_update.email = edit_form.email.data

        # Updating db
        try:
            db.session.commit()
            flash('User Updated!')
            return redirect(url_for('main.user_profile'))
        except:
            db.session.rollback()
            flash('Update failed! Try again...')
            return redirect(url_for('main.user_dashboard'))

    #TODO: Add update logic
    return render_template('/users/user_edit.html', edit_form=edit_form, delete_form=delete_form)

@main_bp.route('/user/delete/<int:id>', methods=["POST"])
@login_required
def user_delete(id):
    user_to_delete = Users.query.get_or_404(id)

    # Only correct user can delete
    if not current_user.id == id:
        flash('Unauthorized access!')
        return redirect(url_for('main.user_dashboard'))
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('Profile Deleted!')
        #TODO: Add admin logic here to add proper routing
        if False:
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'User Deletion Failed! | Error: {e}')
        #TODO: Add admin logic here to add proper routing
        if False:
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.user_dashboard'))
        
# Change user pass route
@main_bp.route('/user/password/update', methods=["GET", "POST"])
@login_required
def user_update_pass():
    form = UpdateUserPass()
    user_to_update = current_user

    """ NO LONGER NEEDED 
    if not current_user.id == id:
        flash('Unauthorized access!')
        return redirect(url_for('main.user_dashboard'))
    """

    # Adding multiple conditions for security
    if request.method == "POST" and form.validate_on_submit():
        # Validating current pass matches
        if not check_password_hash(user_to_update.password_hash, form.current_password.data):
            flash('Current password incorrect.')
            return redirect(url_for('main.user_update_pass'))
        
        # Prevent reusing old password
        if check_password_hash(user_to_update.password_hash, form.password.data):
            flash('New password must be different from the current one.')
            return redirect(url_for('main.user_update_pass'))

        # Hash and update
        user_to_update.password_hash = generate_password_hash(form.password.data)

        try: 
            db.session.commit()
            flash('Password updated successfully.')
            return redirect(url_for('main.user_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating the password.')
            return redirect(url_for('main.user_dashboard'))
        
    return render_template('/users/user_update_pass.html', form=form)


""" Tasks: CRUD Ops """
#TODO: ALL

# Create
@main_bp.route('/user/task/add', methods=["GET", "POST"])
def task_create():
    form = CreateTask()

    if request.method == "POST":
        
        # Handling blanks 
        due_date = form.due_date.data or date.today()
        due_time = form.due_time.data or None  # optional, can be left NULL

        # Manually validating user title
        title = (form.title.data or "").strip()
        notes = (form.notes.data or "").strip()
        if not title:
            flash('Task cannot be created without a "Title"')
            return redirect(url_for('main.task_list'))

        if len(notes) > 500:
            flash('"Notes" too long! Max length 500')
            return redirect(url_for('main.task_list'))

        # Adding to DB here
        task = Tasks(
            title=form.title.data,
            notes=form.notes.data,
            due_date=due_date,
            due_time=due_time,
            user_id=current_user.id
        )

        # Adding to DB
        db.session.add(task)
        db.session.commit()

        # flash & redirect
        flash('Task added successfully!')
        return redirect(url_for('main.task_list'))
    
    # GET
    return render_template('/tasks/task_create.html', form=form)

# Read: Details for a single task
@main_bp.route('/user/tasks/<int:id>')
def task_detail(id):
    return True

# View all tasks
@main_bp.route('/user/tasks')
def task_list():
    #TODO: Show all past and future tasks
    tasks = Tasks.query.filter_by(user_id=current_user.id).order_by(Tasks.due_date.asc()).all()

    return render_template('tasks/task_list.html', tasks=tasks)

# Update
@main_bp.route('/user/tasks/edit/<int:id>')
def task_edit(id):
    return True

# Deletion
@main_bp.route('/user/task/delete')
def task_delete():
    return True

