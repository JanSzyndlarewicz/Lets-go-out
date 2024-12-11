import json

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.form import _Auto
from wtforms import IntegerField, RadioField, SelectMultipleField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Optional

from app import db
from app.forms.validators import age_limit
from app.models import Interest


class ProfileManagerForm(FlaskForm):
    name = StringField("Name", [InputRequired(message="Name must not be empty.")])
    gender = RadioField("Gender")
    description = TextAreaField("Description", [])
    gender_preferences = SelectMultipleField("Gender preferences")
    year_of_birth = IntegerField("Year of birth", [InputRequired(message="Year of birth is required."), age_limit])
    lower_difference = IntegerField(
        "Lower Difference",
        [
            InputRequired(message="Age difference is required."),
            NumberRange(min=0, max=30, message="Age difference cannot be negative."),
        ],
    )
    upper_difference = IntegerField(
        "Upper Difference",
        [
            InputRequired(message="Age difference is required."),
            NumberRange(min=0, max=30, message="Age difference cannot be negative."),
        ],
    )
    photo = FileField("Profile Photo", validators=[Optional()])
    submit = SubmitField("Change")
    interests = StringField("Interests", validators=[Optional()])

    @property
    def interests_as_list(self):
        return [db.get_or_404(Interest, int(single["id"])) for single in json.loads(self.interests.data)]
