from functools import wraps

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import User, db
from app.forms import LoginForm, RegisterForm
from app.utils import send_email

auth_bp = Blueprint("auth_bp", __name__)


# only allow confirmed users, otherwise redirect to unconfirmeed page
def confirmed_required(func):
    @wraps(func)
    @login_required
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if not current_user.confirmed:
            return redirect(url_for("auth_bp.unconfirmed"))
        return func(*args, **kwargs)

    return inner


# only allow unconfirmed users, otherwise redirect to main page
def unconfirmed_required(func):
    @wraps(func)
    @login_required
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if current_user.confirmed:
            return redirect(url_for("find_page_bp.find_page"))
        return func(*args, **kwargs)

    return inner


# only allow for anonymous (unlogged) users, otherwise redirect to main page
def anonymous_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if not current_user.is_anonymous:
            return redirect(url_for("find_page_bp.find_page"))
        return func(*args, **kwargs)

    return inner


# THIS IS EXCLUSIVELY FOR TESTING AND MUST BE REMOVED IN THE FINAL VERSION
@auth_bp.route("/forced_entry", methods=["POST"])
def forced_entry():
    user = User.query.first()
    user.confirmed = True
    db.session.commit()
    login_user(user)
    return redirect(url_for("find_page_bp.find_page"))


@auth_bp.route("/login", methods=["GET", "POST"])
@anonymous_required
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("find_page_bp.find_page"))
        return "Invalid credentials", 401

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@anonymous_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        token = new_user.generate_token()
        confirm_url = url_for("auth_bp.confirm", token=token, _external=True)
        contents = render_template("confirmation_email.html", url=confirm_url)
        subject = "Email confirmation"

        send_email(email, subject, contents)

        login_user(new_user)
        return redirect(url_for("auth_bp.unconfirmed"))

    return render_template("register.html", form=form)


@auth_bp.route("/confirm/<token>", methods=["GET", "POST"])
@unconfirmed_required
def confirm(token):
    if current_user.confirm(token):
        db.session.commit()
        return redirect(url_for("find_page_bp.find_page"))
    flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("auth_bp.unconfirmed"))


@auth_bp.route("/unconfirmed")
@unconfirmed_required
def unconfirmed():
    return render_template("unconfirmed.html")


@auth_bp.route("/resend")
@unconfirmed_required
def resend():
    token = current_user.generate_token()
    confirm_url = url_for("auth_bp.confirm", token=token, _external=True)
    contents = render_template("confirmation_email.html", url=confirm_url)
    subject = "Email confirmation"

    send_email(current_user.email, subject, contents)

    return redirect(url_for("auth_bp.unconfirmed"))
