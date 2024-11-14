from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app import User, db
from app.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("find_page_bp.find_page"))
        return "Invalid credentials", 401

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("find_page_bp.find_page"))

    return render_template("register.html", form=form)
