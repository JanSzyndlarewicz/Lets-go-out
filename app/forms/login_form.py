from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField(
        "User name",
        [InputRequired(message="You must provide a username to log in.")],
    )
    password = PasswordField(
        "Password",
        [InputRequired(message="You must provide a password to log in.")],
    )
    submit = SubmitField("Submit")
