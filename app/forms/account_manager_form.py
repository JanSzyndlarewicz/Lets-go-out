from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class AccountManagerForm(FlaskForm):
    email = EmailField(
        "Email",
        [
            InputRequired(message="Email address is required."),
            Email(message="Please provide a correct email address."),
        ],
    )
    old_password = PasswordField(
        "Current password:",
        [InputRequired(message="Please input your current password.")],
    )
    new_password = PasswordField(
        "New password",
        [
            InputRequired(message="Please input new password."),
            Length(min=1, message="Password is too short!"),
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
