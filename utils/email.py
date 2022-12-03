import os

from flask_mail import Mail, Message
from flask import render_template

from utils.helper import get_reset_token

mail = Mail()


def send_change_password_email(user):
    token = get_reset_token(user)
    msg = Message()
    msg.subject = "Learning Together password reset request"
    msg.sender = os.getenv('MAIL_USERNAME')
    msg.recipients = [user.email]
    msg.html = render_template('email_templates/change_email.html', token=token, name=user.user_name, _external=True)
    mail.send(msg)
