from datetime import datetime

from flask_pagedown.fields import PageDownField
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SubmitField,PasswordField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError

from app.models import Author, db, Comment, Post


class CommentForm(FlaskForm):
    username=StringField('UserName',validators=[Length(min=4,max=25),Regexp('[0-9a-zA-Z]',)])
    email = StringField('Email Address',validators=[Length(min=6, max=35)] )
    content=TextAreaField('Comment')

    def create_form(self,post_id):
        new_comment = Comment()
        new_comment.author_name = self.username.data
        new_comment.author_email = self.email.data
        new_comment.create_time = datetime.utcnow()
        new_comment.content = self.content.data
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()

class LoginForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(message='Username Error')])
    password=PasswordField('密码',validators=[DataRequired(message='Password Error')],)

    def validate_username(self,field):
        if field.data and not Author.query.filter_by(username=field.data).first():
            raise ValidationError('Username Error')

    def validate_password(self,field):
        author=Author.query.filter_by(username=self.username.data).first()
        if author and not author.check_password(field.data):
            raise ValidationError('Password Error')




class RegisterForm(FlaskForm):
    username=StringField('UserName')
    email=StringField('Email')
    password=PasswordField('password')
    repassword=PasswordField('password',validators=[EqualTo('password')])

    def validate_username(self,field):
        if Author.query.filter_by(username=field.data).first():
            raise  ValidationError('username use')

    def validate_email(self,field):
        if Author.query.filter_by(email=field.data).first():
            raise  ValidationError('email use')

    def create_author(self):
        author=Author()
        author.username=self.username.data
        author.password=self.password.data
        author.email=self.email.data
        db.session.add(author)
        db.session.commit()
        return author
class PostForm(FlaskForm):
    title=StringField('标题')
    content=PageDownField('内容')

    def create_post(self,author_id):
        post=Post()
        post.author_id=author_id
        self.populate_obj(post)
        # post.title=self.title.data
        # post.content=self.content.data
        # post.author_id=author_id
        # post.category_id=category_id
        # post.tag=tag
        db.session.add(post)
        db.session.commit()
        return post
    def update_post(self,post):
        self.populate_obj(post)
        db.session.add(post)
        db.session.commit()
        return post
