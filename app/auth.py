from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, User
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        
        print(username)

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for('dashboard_bp.dashboard'))
        return "Invalid credentials", 401

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        
        password_hash = generate_password_hash(password)

        # Create new user
        new_user = User(username=username, password=password_hash, email=email)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('dashboard_bp.dashboard'))

    return render_template('register.html', form=form)