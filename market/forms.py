from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Length, Email , EqualTo

class RegisterForm(FlaskForm):
    username= StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email_address=StringField('Email',validators=[DataRequired(),Email()])
    password1=PasswordField('Password1',validators=[DataRequired(), Length(min=6)])
    password2=PasswordField('Password2',validators=[DataRequired(), Length(min=6) , EqualTo('password1', message='Passwords must match')])
    submit=SubmitField('Create Acount')
