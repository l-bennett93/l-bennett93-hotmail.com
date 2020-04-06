from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired(), EqualTo("password_check")])
    password_check = PasswordField("Password Check", validators = [DataRequired()])
    submit = SubmitField("Register")

    def check_email(self, field):
        if User.query.filter_by(email = field.data):
            ValidationError("This email has already been registered")

    def check_username(self, field):
        if User.query.filter_by(username = field.data):
            ValidationError("This username has already been registered")

class UserLoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Log In")
