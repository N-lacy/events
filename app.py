# # import logging
# # import os
# # from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_file
# # from flask_sqlalchemy import SQLAlchemy
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# # from flask_bcrypt import Bcrypt
# # import random
# # import qrcode
# # from io import BytesIO
# # import uuid
# # from datetime import datetime

# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'your_secret_key'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # db = SQLAlchemy(app)
# # login_manager = LoginManager(app)
# # bcrypt = Bcrypt(app)

# # class User(db.Model, UserMixin):
# #     id = db.Column(db.Integer, primary_key=True)
# #     username = db.Column(db.String(150), nullable=False, unique=True)
# #     password = db.Column(db.String(150), nullable=False)

# # class Student(db.Model):
# #     id = db.Column(db.String(50), primary_key=True)
# #     name = db.Column(db.String(100), nullable=False)
# #     passport_number = db.Column(db.String(50), nullable=True)
# #     phone_number = db.Column(db.String(20), nullable=True)

# # class Event(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     event_id = db.Column(db.String(50), nullable=False, unique=True)
# #     event_name = db.Column(db.String(100), nullable=False)
# #     required_fields = db.Column(db.String(500), nullable=False)
# #     mandatory_students = db.Column(db.String(500), nullable=True)
# #     event_date = db.Column(db.String(50), nullable=False)
# #     num_students = db.Column(db.Integer, nullable=False)

# # class Application(db.Model):
# #     id = db.Column(db.Integer, primary_key=True)
# #     student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
# #     event_id = db.Column(db.String(50), db.ForeignKey('event.event_id'), nullable=False)
# #     student = db.relationship('Student', backref=db.backref('applications', lazy=True))
# #     event = db.relationship('Event', backref=db.backref('applications', lazy=True))

# # @login_manager.user_loader
# # def load_user(user_id):
# #     return User.query.get(int(user_id))

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         user = User.query.filter_by(username=username).first()
# #         if user and bcrypt.check_password_hash(user.password, password):
# #             login_user(user)
# #             return redirect(url_for('admin'))
# #         else:
# #             flash('Login Unsuccessful. Please check username and password', 'danger')
# #     return render_template('login.html')

# # @app.route('/logout')
# # @login_required
# # def logout():
# #     logout_user()
# #     return redirect(url_for('login'))

# # @app.route('/admin')
# # @login_required
# # def admin():
# #     events = Event.query.all()
# #     return render_template('admin.html', events=events)

# # @app.route('/create_event', methods=['POST'])
# # @login_required
# # def create_event():
# #     try:
# #         event_name = request.json['event_name']
# #         required_fields = request.json['required_fields']
# #         mandatory_students = request.json.get('mandatory_students', '')
# #         event_date = request.json['event_date']
# #         num_students = request.json['num_students']

# #         # Generate unique event ID
# #         now = datetime.now()
# #         event_id = f"{now.strftime('%Y%m')}{uuid.uuid4().hex[:6]}"

# #         new_event = Event(event_id=event_id, event_name=event_name, required_fields=','.join(required_fields), mandatory_students=','.join(mandatory_students), event_date=event_date, num_students=num_students)
# #         db.session.add(new_event)
# #         db.session.commit()

# #         # Ensure QR code directory exists
# #         qr_dir = os.path.join(app.root_path, 'static', 'qr_codes')
# #         if not os.path.exists(qr_dir):
# #             os.makedirs(qr_dir)

# #         # Generate QR code
# #         event_url = f"http://localhost:5000/event/{event_id}"
# #         qr = qrcode.make(event_url)
# #         qr_filename = f"{event_id}_qr.png"
# #         qr_filepath = os.path.join(qr_dir, qr_filename)
# #         qr.save(qr_filepath)

# #         return jsonify({'status': 'Event created', 'qr_code_url': url_for('static', filename=f'qr_codes/{qr_filename}')})

# #     except Exception as e:
# #         logging.error(f"Error creating event: {e}")
# #         return jsonify({'status': 'Error creating event', 'error': str(e)}), 500

# # @app.route('/apply', methods=['GET', 'POST'])
# # def apply():
# #     if request.method == 'GET':
# #         # Render the application form
# #         event_id = request.args.get('event_id')
# #         event = Event.query.filter_by(event_id=event_id).first()
# #         if event:
# #             return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)
# #         else:
# #             return render_template('404.html'), 404

# #     # Extract student information from the request
# #     data = request.get_json()
# #     student_id = data.get('student_id')
# #     event_id = data.get('event_id')
# #     student_name = data.get('student_info').get('name')
# #     student_passport_number = data.get('student_info').get('passport_number')
# #     student_phone_number = data.get('student_info').get('phone_number')

# #     # Ensure all required fields are provided
# #     if not student_id or not event_id or not student_name:
# #         return jsonify({'status': 'Error', 'message': 'Student ID, Event ID, and Name are required'}), 400

# #     student = Student.query.filter_by(id=student_id).first()
# #     if not student:
# #         student = Student(id=student_id, name=student_name, passport_number=student_passport_number, phone_number=student_phone_number)
# #     else:
# #         student.name = student_name
# #         student.passport_number = student_passport_number
# #         student.phone_number = student_phone_number

# #     db.session.add(student)
# #     db.session.commit()

# #     # Register application for the event
# #     application = Application(student_id=student_id, event_id=event_id)
# #     db.session.add(application)
# #     db.session.commit()

# #     return jsonify({'status': 'Application received'})


# # @app.route('/events', methods=['GET'])
# # def events():
# #     events = Event.query.all()
# #     return render_template('events.html', events=events)

# # @app.route('/event/<event_id>', methods=['GET'])
# # def event(event_id):
# #     event = Event.query.filter_by(event_id=event_id).first()
# #     if not event:
# #         return render_template('404.html'), 404
# #     return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)

# # @app.route('/select_students', methods=['POST'])
# # def select_students():
# #     event_id = request.json['event_id']
# #     event = Event.query.filter_by(event_id=event_id).first()
# #     num_students = event.num_students

# #     applications = Application.query.filter_by(event_id=event_id).all()
# #     student_ids = [app.student_id for app in applications]

# #     # Generate final list of selected students
# #     mandatory_students = event.mandatory_students.split(',') if event.mandatory_students else []
# #     selected_students = list(mandatory_students)
# #     remaining_slots = num_students - len(mandatory_students)

# #     weights = [(1 if student_id in mandatory_students else 1.5) for student_id in student_ids]
# #     selected_students += random.choices(student_ids, weights=weights, k=remaining_slots)

# #     return jsonify({'selected_students': selected_students})

# # @app.route('/generate_qr/<event_id>', methods=['GET'])
# # def generate_qr(event_id):
# #     event_url = f"http://localhost:5000/event/{event_id}"
# #     qr = qrcode.make(event_url)
    
# #     buffer = BytesIO()
# #     qr.save(buffer, 'PNG')
# #     buffer.seek(0)
    
# #     return send_file(buffer, mimetype='image/png')

# # @app.route('/schema')
# # def schema():
# #     from sqlalchemy import inspect
# #     inspector = inspect(db.engine)
# #     schema_info = inspector.get_columns('event')
# #     return jsonify(schema_info)

# # if __name__ == '__main__':
# #     with app.app_context():
# #         db.create_all()
# #     app.run(debug=True)


# import logging
# import os
# from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_file
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_bcrypt import Bcrypt
# import random
# import qrcode
# from io import BytesIO
# import uuid
# from datetime import datetime

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# login_manager = LoginManager(app)
# bcrypt = Bcrypt(app)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(150), nullable=False)

# class Student(db.Model):
#     id = db.Column(db.String(50), primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     passport_number = db.Column(db.String(50), nullable=True)
#     phone_number = db.Column(db.String(20), nullable=True)

# class Event(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.String(50), nullable=False, unique=True)
#     event_name = db.Column(db.String(100), nullable=False)
#     required_fields = db.Column(db.String(500), nullable=False)
#     mandatory_students = db.Column(db.String(500), nullable=True)
#     event_date = db.Column(db.String(50), nullable=False)
#     num_students = db.Column(db.Integer, nullable=False)

# class Application(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
#     event_id = db.Column(db.String(50), db.ForeignKey('event.event_id'), nullable=False)
#     student = db.relationship('Student', backref=db.backref('applications', lazy=True))
#     event = db.relationship('Event', backref=db.backref('applications', lazy=True))

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and bcrypt.check_password_hash(user.password, password):
#             login_user(user)
#             return redirect(url_for('admin'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# @app.route('/admin')
# @login_required
# def admin():
#     events = Event.query.all()
#     return render_template('admin.html', events=events)

# @app.route('/view_applicants/<event_id>', methods=['GET'])
# @login_required
# def view_applicants(event_id):
#     event = Event.query.filter_by(event_id=event_id).first()
#     if not event:
#         return render_template('404.html'), 404
#     applications = Application.query.filter_by(event_id=event_id).all()
#     return render_template('view_applicants.html', event=event, applications=applications)

# @app.route('/create_event', methods=['POST'])
# @login_required
# def create_event():
#     try:
#         event_name = request.json['event_name']
#         required_fields = request.json['required_fields']
#         mandatory_students = request.json.get('mandatory_students', '')
#         event_date = request.json['event_date']
#         num_students = request.json['num_students']

#         # Generate unique event ID
#         now = datetime.now()
#         event_id = f"{now.strftime('%Y%m')}{uuid.uuid4().hex[:6]}"

#         new_event = Event(event_id=event_id, event_name=event_name, required_fields=','.join(required_fields), mandatory_students=','.join(mandatory_students), event_date=event_date, num_students=num_students)
#         db.session.add(new_event)
#         db.session.commit()

#         # Ensure QR code directory exists
#         qr_dir = os.path.join(app.root_path, 'static', 'qr_codes')
#         if not os.path.exists(qr_dir):
#             os.makedirs(qr_dir)

#         # Generate QR code
#         event_url = f"http://localhost:5000/event/{event_id}"
#         qr = qrcode.make(event_url)
#         qr_filename = f"{event_id}_qr.png"
#         qr_filepath = os.path.join(qr_dir, qr_filename)
#         qr.save(qr_filepath)

#         return jsonify({'status': 'Event created', 'qr_code_url': url_for('static', filename=f'qr_codes/{qr_filename}')})

#     except Exception as e:
#         logging.error(f"Error creating event: {e}")
#         return jsonify({'status': 'Error creating event', 'error': str(e)}), 500

# @app.route('/apply', methods=['GET', 'POST'])
# def apply():
#     if request.method == 'GET':
#         # Render the application form
#         event_id = request.args.get('event_id')
#         event = Event.query.filter_by(event_id=event_id).first()
#         if event:
#             return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)
#         else:
#             return render_template('404.html'), 404

#     # Extract student information from the request
#     data = request.get_json()
#     student_id = data.get('student_id')
#     event_id = data.get('event_id')
#     student_name = data.get('student_info').get('name')
#     student_passport_number = data.get('student_info').get('passport_number')
#     student_phone_number = data.get('student_info').get('phone_number')

#     # Ensure all required fields are provided
#     if not student_id or not event_id or not student_name:
#         return jsonify({'status': 'Error', 'message': 'Student ID, Event ID, and Name are required'}), 400

#     student = Student.query.filter_by(id=student_id).first()
#     if not student:
#         student = Student(id=student_id, name=student_name, passport_number=student_passport_number, phone_number=student_phone_number)
#     else:
#         student.name = student_name
#         student.passport_number = student_passport_number
#         student.phone_number = student_phone_number

#     db.session.add(student)
#     db.session.commit()

#     # Register application for the event
#     application = Application(student_id=student_id, event_id=event_id)
#     db.session.add(application)
#     db.session.commit()

#     return jsonify({'status': 'Application received'})

# @app.route('/events', methods=['GET'])
# def events():
#     events = Event.query.all()
#     return render_template('events.html', events=events)

# @app.route('/event/<event_id>', methods=['GET'])
# def event(event_id):
#     event = Event.query.filter_by(event_id=event_id).first()
#     if not event:
#         return render_template('404.html'), 404
#     return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)

# @app.route('/select_students', methods=['POST'])
# def select_students():
#     event_id = request.json['event_id']
#     event = Event.query.filter_by(event_id=event_id).first()
#     num_students = event.num_students

#     applications = Application.query.filter_by(event_id=event_id).all()
#     student_ids = [app.student_id for app in applications]

#     # Generate final list of selected students
#     mandatory_students = event.mandatory_students.split(',') if event.mandatory_students else []
#     selected_students = list(mandatory_students)
#     remaining_slots = num_students - len(mandatory_students)

#     weights = [(1 if student_id in mandatory_students else 1.5) for student_id in student_ids]
#     selected_students += random.choices(student_ids, weights=weights, k=remaining_slots)

#     return jsonify({'selected_students': selected_students})

# @app.route('/generate_qr/<event_id>', methods=['GET'])
# def generate_qr(event_id):
#     event_url = f"http://localhost:5000/event/{event_id}"
#     qr = qrcode.make(event_url)
    
#     buffer = BytesIO()
#     qr.save(buffer, 'PNG')
#     buffer.seek(0)
    
#     return send_file(buffer, mimetype='image/png')

# @app.route('/schema')
# def schema():
#     from sqlalchemy import inspect
#     inspector = inspect(db.engine)
#     schema_info = inspector.get_columns('event')
#     return jsonify(schema_info)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
import logging
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import random
import qrcode
from io import BytesIO
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(50), nullable=False, unique=True)
    event_name = db.Column(db.String(100), nullable=False)
    required_fields = db.Column(db.String(500), nullable=False)
    mandatory_students = db.Column(db.String(500), nullable=True)
    event_date = db.Column(db.String(50), nullable=False)
    num_students = db.Column(db.Integer, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.String(50), db.ForeignKey('event.event_id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    event = db.relationship('Event', backref=db.backref('applications', lazy=True))
    is_selected = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    events = Event.query.all()
    return render_template('admin.html', events=events)

@app.route('/view_applicants/<event_id>', methods=['GET'])
@login_required
def view_applicants(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        return render_template('404.html'), 404
    applications = Application.query.filter_by(event_id=event_id).all()
    return render_template('view_applicants.html', event=event, applications=applications)

# @app.route('/create_event', methods=['POST'])
# # @login_required
# def create_event():
#     try:
#         event_name = request.json['event_name']
#         required_fields = request.json['required_fields']
#         mandatory_students = request.json.get('mandatory_students', '')
#         event_date = request.json['event_date']
#         num_students = request.json['num_students']

#         # Generate unique event ID
#         now = datetime.now()
#         event_id = f"{now.strftime('%Y%m')}{uuid.uuid4().hex[:6]}"

#         new_event = Event(event_id=event_id, event_name=event_name, required_fields=','.join(required_fields), mandatory_students=','.join(mandatory_students), event_date=event_date, num_students=num_students)
#         db.session.add(new_event)
#         db.session.commit()

#         # Ensure QR code directory exists
#         qr_dir = os.path.join(app.root_path, 'static', 'qr_codes')
#         if not os.path.exists(qr_dir):
#             os.makedirs(qr_dir)

#         # Generate QR code
#         event_url = f"http://localhost:5000/event/{event_id}"
#         qr = qrcode.make(event_url)
#         qr_filename = f"{event_id}_qr.png"
#         qr_filepath = os.path.join(qr_dir, qr_filename)
#         qr.save(qr_filepath)

#         return jsonify({'status': 'Event created', 'qr_code_url': url_for('static', filename=f'qr_codes/{qr_filename}')})

#     except Exception as e:
#         logging.error(f"Error creating event: {e}")
#         return jsonify({'status': 'Error creating event', 'error': str(e)}), 500


@app.route('/create_event', methods=['POST'])
# @login_required
def create_event():
    try:
        event_name = request.json['event_name']
        required_fields = request.json['required_fields']
        mandatory_students = request.json.get('mandatory_students', '')
        event_date = request.json['event_date']
        num_students = request.json['num_students']

        # Ensure required_fields and mandatory_students are stored as comma-separated strings
        if isinstance(required_fields, list):
            required_fields = ','.join(required_fields)
        if isinstance(mandatory_students, list):
            mandatory_students = ','.join(mandatory_students)

        # Generate unique event ID
        now = datetime.now()
        event_id = f"{now.strftime('%Y%m')}{uuid.uuid4().hex[:6]}"

        new_event = Event(event_id=event_id, event_name=event_name, required_fields=required_fields, mandatory_students=mandatory_students, event_date=event_date, num_students=num_students)
        db.session.add(new_event)
        db.session.commit()

        # Ensure QR code directory exists
        qr_dir = os.path.join(app.root_path, 'static', 'qr_codes')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)

        # Generate QR code
        event_url = f"http://localhost:5000/event/{event_id}"
        qr = qrcode.make(event_url)
        qr_filename = f"{event_id}_qr.png"
        qr_filepath = os.path.join(qr_dir, qr_filename)
        qr.save(qr_filepath)

        return jsonify({'status': 'Event created', 'qr_code_url': url_for('static', filename=f'qr_codes/{qr_filename}')})

    except Exception as e:
        logging.error(f"Error creating event: {e}")
        return jsonify({'status': 'Error creating event', 'error': str(e)}), 500



@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'GET':
        # Render the application form
        event_id = request.args.get('event_id')
        event = Event.query.filter_by(event_id=event_id).first()
        if event:
            return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)
        else:
            return render_template('404.html'), 404

    # Extract student information from the request
    data = request.get_json()
    student_id = data.get('student_id')
    event_id = data.get('event_id')
    student_name = data.get('student_info').get('name')
    student_passport_number = data.get('student_info').get('passport_number')
    student_phone_number = data.get('student_info').get('phone_number')

    # Ensure all required fields are provided
    if not student_id or not event_id or not student_name:
        return jsonify({'status': 'Error', 'message': 'Student ID, Event ID, and Name are required'}), 400

    # Check if the student has already applied for the event
    existing_application = Application.query.filter_by(student_id=student_id, event_id=event_id).first()
    if existing_application:
        return jsonify({'status': 'Error', 'message': 'You have already applied for this event'}), 400

    student = Student.query.filter_by(id=student_id).first()
    if not student:
        student = Student(id=student_id, name=student_name, passport_number=student_passport_number, phone_number=student_phone_number)
    else:
        student.name = student_name
        student.passport_number = student_passport_number
        student.phone_number = student_phone_number

    db.session.add(student)
    db.session.commit()

    # Register application for the event
    application = Application(student_id=student_id, event_id=event_id)
    db.session.add(application)
    db.session.commit()

    return jsonify({'status': 'Application received'})

@app.route('/events', methods=['GET'])
def events():
    events = Event.query.all()
    return render_template('events.html', events=events)

@app.route('/event/<event_id>', methods=['GET'])
def event(event_id):
    event = Event.query.filter_by(event_id=event_id).first()
    if not event:
        return render_template('404.html'), 404
    return render_template('event_application.html', event_name=event.event_name, event_date=event.event_date, event_id=event.event_id)

@app.route('/select_students', methods=['POST'])
def select_students():
    event_id = request.json['event_id']
    event = Event.query.filter_by(event_id=event_id).first()
    num_students = event.num_students

    applications = Application.query.filter_by(event_id=event_id).all()
    student_ids = [app.student_id for app in applications]

    # Generate final list of selected students
    mandatory_students = event.mandatory_students.split(',') if event.mandatory_students else []
    selected_students = list(mandatory_students)
    remaining_slots = num_students - len(mandatory_students)

    weights = [(1 if student_id in mandatory_students else 1.5) for student_id in student_ids]
    selected_students += random.choices(student_ids, weights=weights, k=remaining_slots)

    # Mark selected students in the database
    for student_id in selected_students:
        application = Application.query.filter_by(student_id=student_id, event_id=event_id).first()
        if application:
            application.is_selected = True
            db.session.commit()

    return jsonify({'selected_students': selected_students})

@app.route('/generate_qr/<event_id>', methods=['GET'])
def generate_qr(event_id):
    event_url = f"http://localhost:5000/event/{event_id}"
    qr = qrcode.make(event_url)
    
    buffer = BytesIO()
    qr.save(buffer, 'PNG')
    buffer.seek(0)
    
    return send_file(buffer, mimetype='image/png')

@app.route('/schema')
def schema():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    schema_info = inspector.get_columns('event')
    return jsonify(schema_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
