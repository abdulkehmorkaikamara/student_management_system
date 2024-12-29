# app/routes.py

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from app import db
from app.forms import CourseForm
from app.models import Course

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title='Home')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    return render_template('dashboard.html', title='Dashboard', courses=courses)

@main_bp.route('/add_course', methods=['GET', 'POST'])
@login_required
def add_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!')
        return redirect(url_for('main.dashboard'))
    return render_template('add_course.html', title='Add Course', form=form)

@main_bp.route('/drop_course/<int:course_id>', methods=['POST'])
@login_required
def drop_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course in current_user.courses:
        current_user.courses.remove(course)
        db.session.commit()
        flash('Course dropped successfully!')
    else:
        flash('You are not enrolled in this course.')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/enroll_course/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course not in current_user.courses:
        current_user.courses.append(course)
        db.session.commit()
        flash('Enrolled in course successfully!')
    else:
        flash('Already enrolled in this course.')
    return redirect(url_for('main.dashboard'))



@main_bp.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data)
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('create_course.html', title='Create Course', form=form)