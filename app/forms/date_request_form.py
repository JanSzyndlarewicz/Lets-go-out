from flask_wtf import FlaskForm
from wtforms import DateField, StringField
from wtforms.validators import DataRequired, InputRequired


class DateRequestForm(FlaskForm):
    message = StringField(
        "Optional text attached to accept/reject/reschedule",
        validators=[InputRequired(message="Message can't be empty.")],
    )
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])

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
        self.process()
