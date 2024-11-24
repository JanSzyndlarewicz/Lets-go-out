from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, StringField, SubmitField
from wtforms.fields.choices import SelectMultipleField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ProfileDataFulfilment(FlaskForm):
    name = StringField("Name", [InputRequired(message="Name must not be empty.")])
    gender = RadioField("Gender")
    year_of_birth = IntegerField(
        "Year of birth", [InputRequired(message="Year of birth is required.")]
    )
    gender_preferences = SelectMultipleField("Gender preferences")
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
    submit = SubmitField("Submit")
