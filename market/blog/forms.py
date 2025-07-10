from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired, Length

class BlogForm(FlaskForm):
    title = StringField('Blog Name', validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Blog Description', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Blog')