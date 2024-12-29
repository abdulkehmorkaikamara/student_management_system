# app/models.py

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Association Table for Many-to-Many Relationship Between Students and Courses
enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class Student(UserMixin, db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Student can be enrolled in many courses
    courses = db.relationship('Course', secondary=enrollments, backref='students', lazy='dynamic')

    def set_password(self, password):
        """Hashes and sets the student's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Student {self.username}>'

@login.user_loader
def load_user(student_id):
    """Loads the student for Flask-Login."""
    return Student.query.get(int(student_id))

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Course {self.name}>'
