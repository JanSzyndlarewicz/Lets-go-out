from flask import current_app as app
from flask_mail import Message


def send_email(to: str, subject: str, template: str) -> None:
    msg = Message(subject, recipients=[to], html=template, sender=app.config["MAIL_DEFAULT_SENDER"])
    app.mail.send(msg)
