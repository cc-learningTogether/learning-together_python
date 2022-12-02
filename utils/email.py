import os

from flask_mail import Mail, Message
from flask import render_template

from utils.helper import get_reset_token

mail = Mail()


def send_change_password_email(user):
    token = get_reset_token(user)
    msg = Message()
    msg.subject = "Flask App Password Reset"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [os.getenv('MAIL_USERNAME')]
    msg.html = render_template('email_templates/change_email.html', token=token, name=user.user_name, _external=True)
    mail.send(msg)
