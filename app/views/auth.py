from functools import wraps

from flask import Blueprint
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from app import User, db
from app.forms import LoginForm, RegisterForm
from app.forms.user_data_fulfilment import ProfileDataFulfilment
from app.models import Gender, Profile
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
@auth_bp.route("/forced-entry", methods=["POST"])
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
    profile_form = initialize_profile_form()

    step = request.args.get("step", "register")

    if step == "register" and process_registration_form(form):
        return redirect(url_for("auth_bp.register", step="complete-profile"))

    if step == "complete-profile" and process_profile_form(profile_form):
        return redirect(url_for("auth_bp.unconfirmed"))

    return render_template("register.html", form=form, profile_form=profile_form, step=step)


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


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("find_page_bp.find_page"))
    return redirect(url_for("auth_bp.login"))


def initialize_profile_form():
    profile_form = ProfileDataFulfilment()
    profile_form.gender.choices = [(gender.name, gender.value) for gender in Gender]
    profile_form.gender_preferences.choices = [(gender.name, gender.value) for gender in Gender]
    return profile_form


def process_registration_form(form):
    if form.validate_on_submit():
        session["registration_data"] = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
        }
        return True
    return False


def process_profile_form(profile_form):
    if profile_form.validate_on_submit() and "registration_data" in session:
        try:
            new_user = create_user_with_profile(session["registration_data"], profile_form)
            send_confirmation_email(new_user)
            login_user(new_user)  # TODO: Only for development purposes
            session.pop("registration_data", None)
            return True
        except IntegrityError:
            db.session.rollback()
            flash("An error occurred while creating your account.")
    return False


def create_user_with_profile(registration_data, profile_form):
    new_user = User(
        username=registration_data["username"],
        email=registration_data["email"],
        password=registration_data["password"],
    )

    new_user.profile = Profile(
        name=profile_form.name.data,
        gender=Gender[profile_form.gender.data],
        year_of_birth=profile_form.year_of_birth.data,
    )

    new_user.matching_preferences.gender_preferences = [Gender[gp] for gp in profile_form.gender_preferences.data]
    new_user.matching_preferences.lower_difference = profile_form.lower_difference.data
    new_user.matching_preferences.upper_difference = profile_form.upper_difference.data

    db.session.add(new_user)
    db.session.commit()

    return new_user


def send_confirmation_email(user):
    token = user.generate_token()
    confirm_url = url_for("auth_bp.confirm", token=token, _external=True)
    contents = render_template("confirmation_email.html", url=confirm_url)
    subject = "Email confirmation"
    send_email(user.email, subject, contents)
