# app/auth_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import Student  # <-- Renamed import
from urllib.parse import urlparse

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Renamed 'user' to 'student'
        student = Student.query.filter_by(username=form.username.data).first()
        if student and student.check_password(form.password.data):
            login_user(student, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # Security check to prevent open redirects
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.dashboard')
            return redirect(next_page)
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Sign In', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Renamed 'user' to 'student'
        student = Student(username=form.username.data, email=form.email.data)
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered student!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)
