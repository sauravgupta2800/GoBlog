from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField("title",validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Add picture to post',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('Enter the comment', validators=[DataRequired()])
    submit = SubmitField('Comment')