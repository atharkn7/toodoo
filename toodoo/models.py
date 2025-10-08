from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

# Getting from init
from toodoo import db


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(255), nullable=False)  # Stores hashed password
    profile_pic = db.Column(db.String(), nullable=True)

    # Prevents reading the password directly
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    #TODO: Add bcrypt/argon2 password hashing

    # Hashes the password before storing it
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Verifies a plaintext password against the stored hash
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # String representation for easier debugging/logging
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'
