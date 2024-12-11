from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, StringField
from wtforms.validators import DataRequired, InputRequired, Length

from app.config import MAXIMUM_MESSAGE_LENGTH
from app.forms.validators import is_any_table_available_for_date, is_not_past


class DateRequestForm(FlaskForm):
    id = HiddenField()
    message = StringField(
        "Optional text attached to accept/reject/reschedule",
        validators=[
            Length(
                max=MAXIMUM_MESSAGE_LENGTH, message=f"Message may be at most {MAXIMUM_MESSAGE_LENGTH} characters long"
            )
        ],
    )
    date = DateField(
        "Date", format="%Y-%m-%d", validators=[DataRequired(), is_not_past, is_any_table_available_for_date]
    )

    def __init__(self, message_label_text=True, given_date=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not message_label_text:
            self.message.label.text = ""

        if given_date:
            # Modify the date field properties dynamically instead of replacing it
            self.message.label.text = "Optional text attached to accept/reject"
            self.date.render_kw = {
                "readonly": True,
                "value": given_date.strftime("%Y-%m-%d"),
            }  # Makes the field readonly
            self.date.data = given_date  # Pre-fill the field with the given date
        # self.process()
