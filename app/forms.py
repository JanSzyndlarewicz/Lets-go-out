from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, RadioField, TextAreaField, SelectMultipleField, widgets, IntegerField
from wtforms.validators import InputRequired, Length, EqualTo, Email, DataRequired, NumberRange

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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

class ProfileManagerForm(FlaskForm):
    name = StringField('Name', [InputRequired(message="Name must not be empty.")])
    gender = RadioField('Gender')
    description = TextAreaField('Description', [])
    gender_preferences = MultiCheckboxField('Gender preferences')
    lower_difference = IntegerField("Lower age difference", [DataRequired(message="Age difference is required."), NumberRange(min=1, message="Age difference must be positive.")])
    upper_difference = IntegerField("Upper age difference", [DataRequired(message="Age difference is required."), NumberRange(min=1, message="Age difference must be positive.")])
    submit = SubmitField('Change')