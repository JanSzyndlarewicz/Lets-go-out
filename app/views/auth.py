import json
from functools import wraps

from flask import Blueprint, abort
from flask import current_app as app
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from app import User, db
from app.forms import LoginForm, ProfileManagerForm, RegisterForm
from app.models import Gender, Interest, Photo, Profile
from app.utils import send_email

auth_bp = Blueprint("auth_bp", __name__)


# only allow authenticated users, otherwise redirect to login page
def login_redirect(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        if request.method == "GET":
            return redirect(url_for(app.config["LOGIN_PAGE_ROUTE"]))
        abort(401)

    return inner


# only allow confirmed users, otherwise redirect to unconfirmed/login page
def confirmed_required(func):
    @wraps(func)
    @login_redirect
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if not current_user.confirmed:
            if request.method == "GET":
                return redirect(url_for(app.config["UNCONFIRMED_PAGE_ROUTE"]))
            abort(401)
        return func(*args, **kwargs)

    return inner


# only allow unconfirmed users, otherwise redirect to main/login page
def unconfirmed_required(func):
    @wraps(func)
    @login_redirect
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if current_user.confirmed:
            if request.method == "GET":
                return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))
            abort(401)
        return func(*args, **kwargs)

    return inner


# only allow for anonymous (unlogged) users, otherwise redirect to main page
def anonymous_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not app.config["ADVANCED_ACCESS_CONTROL"]:
            return func(*args, **kwargs)
        if not current_user.is_anonymous:
            if request.method == "GET":
                return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))
            abort(401)
        return func(*args, **kwargs)

    return inner


# THIS IS EXCLUSIVELY FOR TESTING AND MUST BE REMOVED IN THE FINAL VERSION
@auth_bp.route("/forced-entry", methods=["POST"])
def forced_entry():
    user = User.query.first()
    user.confirmed = True
    db.session.commit()
    login_user(user)
    return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))


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
            return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))
        flash("Invalid username or password. Please try again.", "error")
        return redirect(url_for("auth_bp.login"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
@anonymous_required
def register():
    form = RegisterForm()

    if request.method == "GET" and "registration_data" in session:
        registration_data = session["registration_data"]
        form.username.data = registration_data.get("username", "")
        form.email.data = registration_data.get("email", "")

    if process_registration_form(form):
        return redirect(url_for("auth_bp.complete_profile"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/complete-profile", methods=["GET", "POST"])
@anonymous_required
def complete_profile():
    if "registration_data" not in session:
        return redirect(url_for("auth_bp.register"))

    profile_form = initialize_profile_form()

    if process_profile_form(profile_form):
        return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))

    return render_template("auth/complete_profile.html", form=profile_form)


@auth_bp.route("/confirm/<token>", methods=["GET", "POST"])
@unconfirmed_required
def confirm(token):
    if current_user.confirm(token):
        db.session.commit()
        return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))
    flash("The confirmation link is invalid or has expired.")
    return redirect(url_for(app.config["UNCONFIRMED_PAGE_ROUTE"]))


@auth_bp.route("/unconfirmed")
@unconfirmed_required
def unconfirmed():
    return render_template("components/unconfirmed.html")


@auth_bp.route("/resend")
@unconfirmed_required
def resend():
    token = current_user.generate_token()
    confirm_url = url_for("auth_bp.confirm", token=token, _external=True)
    contents = render_template("components/confirmation_email.html", url=confirm_url)
    subject = "Email confirmation"

    send_email(current_user.email, subject, contents)

    return redirect(url_for(app.config["UNCONFIRMED_PAGE_ROUTE"]))


@auth_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for(app.config["MAIN_PAGE_ROUTE"]))
    return redirect(url_for("auth_bp.login"))


def initialize_profile_form():
    profile_form = ProfileManagerForm()
    profile_form.gender.choices = [(gender.name, gender.value) for gender in Gender]
    profile_form.gender_preferences.choices = [(gender.name, gender.value) for gender in Gender]
    profile_form.display_photo = url_for("static", filename=app.config["DEFAULT_PHOTO"])
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
            if app.config["ADVANCED_ACCESS_CONTROL"]:
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
        description=profile_form.description.data,
        year_of_birth=profile_form.year_of_birth.data,
        interests=[db.get_or_404(Interest, int(single["id"])) for single in json.loads(profile_form.interests.data)],
    )

    new_user.matching_preferences.gender_preferences = [Gender[gp] for gp in profile_form.gender_preferences.data]
    new_user.matching_preferences.lower_difference = profile_form.lower_difference.data
    new_user.matching_preferences.upper_difference = profile_form.upper_difference.data

    db.session.add(new_user)
    db.session.commit()

    if profile_form.photo.data:
        photo = profile_form.photo.data
        handle_photo_upload(photo, new_user)

    return new_user


def send_confirmation_email(user):
    token = user.generate_token()
    confirm_url = url_for("auth_bp.confirm", token=token, _external=True)
    contents = render_template("components/confirmation_email.html", url=confirm_url)
    subject = "Email confirmation"
    send_email(user.email, subject, contents)


def handle_photo_upload(photo, user) -> Photo:

    extension = secure_filename(photo.filename).split(".")[-1]
    new_photo = Photo(profile=user.profile, file_extension=extension)

    db.session.add(new_photo)
    db.session.commit()

    photo.save(new_photo.os_photo_url)

    user.profile.photo = new_photo

    return new_photo
