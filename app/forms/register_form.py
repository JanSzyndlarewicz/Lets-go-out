from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.config import MINIMUM_PASSWORD_LENGTH
from app.forms.validators import email_unique, username_unique


class RegisterForm(FlaskForm):
    username = StringField("User name", [InputRequired(message="Please input an username."), username_unique])
    password = PasswordField(
        "Password",
        [
            InputRequired(message="Please input the password."),
            Length(min=MINIMUM_PASSWORD_LENGTH, message="Password is too short!"),
        ],
    )
    confirm = PasswordField(
        "Confirm password",
        [
            InputRequired(message="Please confirm the password."),
            EqualTo(
                "password",
                message="Password confirmation must equal the password.",
            ),
        ],
    )
    email = EmailField(
        "Email",
        [
            InputRequired(message="Email address is required."),
            Email(message="Please provide a correct email address."),
            email_unique,
        ],
    )
    submit = SubmitField("Next")
