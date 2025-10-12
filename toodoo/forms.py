from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


# Login User
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=16)])
    login = SubmitField('Login')

# Register new user
class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8, max=16), EqualTo('password2', message='Passwords Must Match')])
    password2 = PasswordField('Confirm Password', validators=[Length(min=8, max=16)])
    register = SubmitField('Register')

# Edit User Form
class EditUser(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    save = SubmitField("Save")

# Delete user
class DeleteForm(FlaskForm):
    delete = SubmitField('Delete')

# Change User Password Form
class UpdateUserPass(FlaskForm):
    current_password = PasswordField('Current Password', validators=[Length(min=8, max=16)])
    password = PasswordField('Password', validators=[Length(min=8, max=16), EqualTo('password2', message='Passwords Must Match')])
    password2 = PasswordField('Confirm Password', validators=[Length(min=8, max=16)])
    submit = SubmitField('Submit')