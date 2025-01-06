import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Bcrypt for password hashing
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Define the User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

# Define the Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(50), nullable=False, unique=True)
    event_name = db.Column(db.String(100), nullable=False)
    required_fields = db.Column(db.String(500), nullable=False)
    mandatory_students = db.Column(db.String(500), nullable=True)
    event_date = db.Column(db.String(50), nullable=False)
    num_students = db.Column(db.Integer, nullable=False)

# Define the Application model
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.String(50), db.ForeignKey('event.event_id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    event = db.relationship('Event', backref=db.backref('applications', lazy=True))

# Create all the tables and add an admin user
with app.app_context():
    db.create_all()

    # Hash the password and add the admin user
    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    admin_user = User(username='admin', password=hashed_password)
    db.session.add(admin_user)
    db.session.commit()

    print("Database created successfully with admin user!")
