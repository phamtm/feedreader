from flask.ext.wtf import Form
from flask.ext.login import current_user
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField)
from wtforms.validators import (Required,
                                EqualTo,
                                Email,
                                Length,
                                ValidationError)

from app.models import User


# Define registration form
class RegisterForm(Form):
    email = StringField(u'Email address',
                        validators=[Required(),
                                    Email(),
                                    Length(max=128)])
    password = PasswordField(
        u'Password',
        validators=[Required(),
                    Length(min=8, max=64),
                    EqualTo('password2', message='Passwords must match')]
    )
    password2 = PasswordField(u'Confirm password')
    submit = SubmitField(u'Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')



# Define login form
class LoginForm(Form):
    email = StringField(u'Email address',
                        validators=[Required(),
                                    Email(),
                                    Length(max=128)])
    password = PasswordField(u'Password',
                             validators=[Required()])
    remember = BooleanField(u'Remember Me')
    submit = SubmitField(u'Log in')



# Define password change form
class ChangePasswordForm(Form):
    old_password = PasswordField(u'Old Password',
                                 validators=[Required()])
    new_password = PasswordField(u'New password',
                                 validators=[Required(),
                                             EqualTo('new_password2'),
                                             Length(min=8, max=64)])
    new_password2 = PasswordField(u'Confirm password')
    submit = SubmitField(u'Change password')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Wrong password')



# Define password reset request form
class ResetPasswordRequestForm(Form):
    email = StringField(u'Email address',
                        validators=[Required(),
                                    Email(),
                                    Length(max=128)])
    submit = SubmitField(u'Submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email doesn\'t exists')



# Password reset form
class ResetPasswordForm(Form):
    new_password = PasswordField(u'New password',
                                 validators=[Required(),
                                             EqualTo('new_password2'),
                                             Length(min=8, max=64)])
    new_password2 = PasswordField(u'Confirm password')
    submit = SubmitField(u'Submit')



class URLForm(Form):
    url = StringField(u'URL', validators = [Required()])
    submit = SubmitField(u'Submit')
