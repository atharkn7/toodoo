from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

# Getting from init
from toodoo import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.now)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_pic = db.Column(db.String(), nullable=True)


    # Password hashing

    # Repr of objects
    def __repr__(self):
        return '<Name %r>' % self.name
