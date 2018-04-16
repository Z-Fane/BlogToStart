import datetime
import os
import random

from flask import Blueprint, render_template, redirect, url_for, request, current_app, make_response
from flask_login import login_required, login_user, current_user, logout_user

import app
from app import Author
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import Post

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        author = Author.query.filter_by(username=form.username.data).first()
        login_user(author, True)
        return redirect(url_for('.index'))
    return render_template('admin/login.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))


@admin.route('/register', methods=['get', 'post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_author()
        return redirect(url_for('.login'))
    return render_template('admin/register.html', form=form)


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/manager')
@login_required
def manager():
    page = request.args.get('page', default=1, type=int)
    # pagination = Post.query.paginate(page=page, per_page=current_app.config['ADMIN_PER_PAGE'], error_out=False)
    posts=Post.query.all()
    return render_template('admin/post_manager.html', posts=posts)
