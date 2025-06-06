from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class Register_form(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    button = SubmitField(label='Submit')


# TODO: Create a LoginForm to login existing users
class Login_form(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    button = SubmitField(label='LOG IN')

# TODO: Create a CommentForm so users can leave comments below posts
class Comment_form(FlaskForm):
    comment = CKEditorField(label='comments')
    submit = SubmitField(label='post comment')