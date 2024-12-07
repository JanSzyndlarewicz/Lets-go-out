from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.forms.validators import email_unique,username_unique


class RegisterForm(FlaskForm):
    username = StringField("User name", [InputRequired(message="Please input an username."), username_unique])
    # minimal password length set to 1 for convenience of testing; set to something like 8 in final version
    password = PasswordField(
        "Password",
        [
            InputRequired(message="Please input the password."),
            Length(min=1, message="Password is too short!"),
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
            email_unique
        ],
    )
    submit = SubmitField("Next")
