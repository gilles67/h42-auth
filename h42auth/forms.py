from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PasswordChange(FlaskForm):
    password_old = PasswordField('Old password', validators=[DataRequired()])
    password_new = PasswordField('New password', validators=[DataRequired()])
    password_check = PasswordField('Repeat New Password', validators=[DataRequired()])
