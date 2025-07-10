from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,TextAreaField
from wtforms.validators import DataRequired, Length, Email , EqualTo , ValidationError

from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_check):
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username_check.data).first()
        if existing_user:
            raise ValidationError('That username is already taken. Please choose a different one.')
        
    def validate_email_address(self, email_check):
        # Check if the email address already exists in the database
        existing_email = User.query.filter_by(email_address=email_check.data).first()
        if existing_email:
            raise ValidationError('That email address is already registered. Please choose a different one.')

    username= StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email_address=StringField('Email',validators=[DataRequired(),Email()])
    password1=PasswordField('Password1',validators=[DataRequired(), Length(min=6)])
    password2=PasswordField('Password2',validators=[DataRequired(), Length(min=6) , EqualTo('password1', message='Passwords must match')])
    submit=SubmitField('Create Acount')



class LoginForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    password=PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    submit=SubmitField('Login')

class BlogForm(FlaskForm):
    title = StringField('Blog Name', validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Blog Description', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Blog')