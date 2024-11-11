from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import User, db

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find user by username
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for("dashboard_bp.dashboard"))
        return "Invalid credentials", 401

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("dashboard_bp.dashboard"))

    return render_template("register.html")
