# import random
# import uuid
# from datetime import datetime
# from app import db, Student, Event, Application

# # Function to generate random student information
# def generate_student(student_id):
#     names = ["Alice", "Bob", "Charlie", "David", "Eve", "Faythe", "Grace", "Heidi", "Ivan", "Judy"]
#     passports = [f"P{random.randint(100000, 999999)}" for _ in range(10)]
#     phones = [f"{random.randint(1000000000, 9999999999)}" for _ in range(10)]
    
#     return Student(
#         id=student_id,
#         name=random.choice(names),
#         passport_number=random.choice(passports),
#         phone_number=random.choice(phones)
#     )

# # Function to create a random event
# def create_event():
#     event_name = f"Event {uuid.uuid4().hex[:6]}"
#     required_fields = ["name", "passport_number", "phone_number"]
#     mandatory_students = [f"{uuid.uuid4().hex[:6]}" for _ in range(random.randint(1, 5))]
#     event_date = datetime.now().strftime("%Y-%m-%d")
#     num_students = random.randint(5, 20)
    
#     event = Event(
#         event_id=uuid.uuid4().hex[:6],
#         event_name=event_name,
#         required_fields=",".join(required_fields),
#         mandatory_students=",".join(mandatory_students),
#         event_date=event_date,
#         num_students=num_students
#     )
#     db.session.add(event)
#     db.session.commit()
#     return event

# # Function to simulate applications
# def simulate_applications(num_events, num_applications_per_event):
#     events = [create_event() for _ in range(num_events)]

#     for event in events:
#         for _ in range(num_applications_per_event):
#             student_id = uuid.uuid4().hex[:6]
#             student = generate_student(student_id)

#             if not Student.query.filter_by(id=student_id).first():
#                 db.session.add(student)
#                 db.session.commit()

#             application = Application(
#                 student_id=student_id,
#                 event_id=event.event_id
#             )

#             if not Application.query.filter_by(student_id=student_id, event_id=event.event_id).first():
#                 db.session.add(application)
#                 db.session.commit()

# if __name__ == "__main__":
#     with db.app.app_context():
#         simulate_applications(num_events=4, num_applications_per_event=30)
#         print("Simulated applications added successfully!")


