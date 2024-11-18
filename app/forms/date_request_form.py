from wsgiref.validate import validator

from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired

class DateRequestForm(FlaskForm):
    message = StringField(
        "Optional text attached to accept/reject/reschedule",
        validators=[InputRequired(message="Message can't be empty.")],
    )
    date = DateField("Date", format="%Y-%m-%d", validators=[DataRequired()])
    # submit_reject = SubmitField("Reject", widget=LabeledIconSubmitWidget())
    # submit_ignore = SubmitField("Ignore", widget=LabeledIconSubmitWidget())
    # submit_reschedule = SubmitField("Reschedule", widget=LabeledIconSubmitWidget())
    # submit_accept = SubmitField("Accept", widget=LabeledIconSubmitWidget())
    # submit_invite = SubmitField("Invite", widget=LabeledIconSubmitWidget())

    def __init__(self, message_label_text=None, given_date=None, *args, **kwargs):
        super(DateRequestForm, self).__init__(*args, **kwargs)
        if message_label_text:
            self.message.label.text = message_label_text
        if given_date:
            self.date = StringField(label=given_date, render_kw={"readonly": True})
