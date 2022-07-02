from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),
        Email(),
        Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(
        min=8, max=64, message='Password length must be between %(min)d and %(max)d characters') ])
    confirm_password = PasswordField(
        label=('Confirm Password'),
        validators=[DataRequired(message='*Required'),
        EqualTo('password', message='Both password fields must be equal!')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_username(self, username):
        excluded_chars = " ,*?!'^+%&/()=}][{$#/\\\""
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")