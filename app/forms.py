from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('User name', [InputRequired(message="You must provide a username to log in.")])
    password = PasswordField('Password', [InputRequired(message="You must provide a password to log in.")])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('User name', [InputRequired(message="Please input an username.")])
    #minimal password length set to 1 for convenience of testing; set to something like 8 in final version
    password = PasswordField('Password', [InputRequired(message="Please input the password."), Length(min=1, message="Password is too short!")])
    confirm = PasswordField('Password', [InputRequired(message="Please confirm the password."), EqualTo('password', message="Password confirmation must equal the password.")])
    email = EmailField('Email', [InputRequired(message="Email address is required."), Email(message="Please provide a correct email address.")])
    submit = SubmitField('Submit')