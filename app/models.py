from linecache import cache

import bleach
from flask import current_app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

from datetime import  datetime

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from markdown import markdown
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
)

class Base(db.Model):
    __abstract__=True
    create_time = db.Column(db.DateTime,default=datetime.utcnow())
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
class Post(Base):
    STATUS_NORMAL=10
    STATUS_HIDDEN=20
    STATUS_DRAUGHT=30
    # 文章ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 文章标题
    title = db.Column(db.String(80))
    # 文章内容
    content = db.Column(db.Text)
    # 文章分类
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('Post', lazy='dynamic'))
    # 作者
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('Post', lazy='dynamic'))
    # 文章标签
    tag = db.relationship('Tag', secondary=tags, backref=db.backref('Post', lazy='dynamic'))
    comments = db.relationship('Comment', backref='Post')
    views=db.Column(db.Integer,default=0)
    status=db.Column(db.Integer,default=STATUS_NORMAL)
    body_html=db.Column(db.Text)


    @staticmethod
    def on_changed_body(target,value,oldvalue,initator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))
db.event.listen(Post.content,'set',Post.on_changed_body)


class Author(Base, UserMixin):
    ROLE_USER = 10
    ROLE_STAFF = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    publish_post = db.relationship('Post')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_staff(self):
        return self.role == self.ROLE_STAFF

    @staticmethod
    def verify_auth_token(token):
        serializer=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user=Author.query.filter_by(id=data['id']).first()
        return user

class Category(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)



class Tag(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False,unique=True)


class Comment(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String(80), nullable=False)
    author_email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
