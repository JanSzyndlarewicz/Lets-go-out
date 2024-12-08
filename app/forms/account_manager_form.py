from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from app.config import MINIMUM_PASSWORD_LENGTH
from app.forms.validators import email_own_or_unique, password_correct


class AccountManagerForm(FlaskForm):
    email = EmailField(
        "Email",
        [
            InputRequired(message="Email address is required."),
            Email(message="Please provide a correct email address."),
            email_own_or_unique
        ],
    )
    old_password = PasswordField(
        "Current password:",
        [InputRequired(message="Please input your current password."), password_correct],
    )
    new_password = PasswordField(
        "New password",
        [
            InputRequired(message="Please input new password."),
            Length(min=MINIMUM_PASSWORD_LENGTH, message="Password is too short!"),
        ],
    )
    new_confirm = PasswordField(
        "Confirm new password",
        [
            InputRequired(message="Please confirm the new password."),
            EqualTo(
                "new_password",
                message="Password confirmation must equal the password.",
            ),
        ],
    )
    submit = SubmitField("Change")
