from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, EmailField, ValidationError
from wtforms.validators import DataRequired
from datetime import datetime


# Register Form
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()],
                           render_kw={"placeholder": "Discord server Username"})
    email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Password', validators=[DataRequired()],
                                     render_kw={"placeholder": "Confirm Password"})
    # TODO set language field to required when database is ready
    language = SelectField("Language", choices=["-", "English/英語", "Japanese/日本語"])
    gender = SelectField("Gender", choices=["-", "Male/男", "Female/女"])
    # TODO set is_supporter field to required when database is ready
    is_supporter = SelectField("Are you a supporter?", choices=["-", "No/いいえ", "Yes/はい"])
    submit_register = SubmitField("Sign Up!")


# Login form

class LoginForm(FlaskForm):
    login_email = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    login_password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit_login = SubmitField("Sign In")


# Require new password form
class ForgotPswForm(FlaskForm):
    email_forgot_password = EmailField("Email", validators=[DataRequired()], render_kw={"placeholder": "Email"})
    submit_forgot_password = SubmitField("Send Email!")


# change password form

class ChangePSWForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Password', validators=[DataRequired()],
                                     render_kw={"placeholder": "Confirm Password"})
    submit_change_password = SubmitField("Submit")


class DateTimeForm(FlaskForm):
    dt_start = StringField("Start at", validators=[DataRequired()])
    dt_finish = StringField("Finish at", validators=[DataRequired()])
    submit_register = SubmitField("Submit")

    def validate_dt_start(self, dt_start):
        # if the user input incorrect datetime 
        date = datetime.strptime(dt_start.data, "%Y/%m/%d %H:%M")
        if ( date - datetime.now() ).total_seconds() < 0 :
            raise ValidationError("Chose later than today")

    def validate_dt_finish(self, dt_finish):
        # if the user input incorrect datetime 
        date = datetime.strptime(dt_finish.data, "%Y/%m/%d %H:%M")
        if ( date - datetime.now() ).total_seconds() < 0 :
            raise ValidationError("Chose later than today")
    
class SearchForm(FlaskForm):
    language = SelectField("*Language", choices=["-", "English/英語", "Japanese/日本語"])
    gender = SelectField("Gender", choices=["-", "Male/男", "Female/女"])
    is_supporter = SelectField("Are you a supporter?", choices=["-", "No/いいえ", "Yes/はい"])
    submit_register = SubmitField("Search")
