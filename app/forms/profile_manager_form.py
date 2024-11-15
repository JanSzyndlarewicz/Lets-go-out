from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, RadioField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ProfileManagerForm(FlaskForm):
    name = StringField("Name", [InputRequired(message="Name must not be empty.")])
    gender = RadioField("Gender")
    description = TextAreaField("Description", [])
    gender_preferences = SelectMultipleField("Gender Preferences")
    lower_difference = IntegerField(
        "Lower age difference",
        [
            DataRequired(message="Age difference is required."),
            NumberRange(min=1, message="Age difference must be positive."),
        ],
    )
    upper_difference = IntegerField(
        "Upper age difference",
        [
            DataRequired(message="Age difference is required."),
            NumberRange(min=1, message="Age difference must be positive."),
        ],
    )
    submit = SubmitField("Change")
