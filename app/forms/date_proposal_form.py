from flask_wtf import FlaskForm
from wtforms import DateField, StringField
from wtforms.validators import DataRequired, InputRequired


class DateProposalForm(FlaskForm):
    message = StringField(
        "Optional text attached to accept/reject/reschedule",
        validators=[InputRequired(message="Message can't be empty.")],
    )
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
