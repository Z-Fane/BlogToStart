from datetime import datetime

from flask import Blueprint, render_template, flash, url_for, redirect
from flask_login import current_user, login_required

from app.forms import CommentForm, PostForm, CategoryForm
from app.models import Comment, db, Post, Category

post = Blueprint('post', __name__, url_prefix='/post')


@post.route('/<int:post_id>', methods=('GET', 'POST'))
def detail(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        form.create_form(post_id)
    post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    return render_template('detail.html', form=form, title="Post", post=post, comments=comments)


@post.route('/create_post', methods=['get', 'post'])
@login_required
def create_post():
    form = PostForm()
    categories=Category.query.all()
    form.category.choices=[(c.name, c.name) for c in categories]
    if form.validate_on_submit():
        form.create_post(current_user.id)
        return redirect(url_for('admin.index'))
    return render_template('admin/create_post.html', form=form, type=0)


@post.route('/<int:post_id>/edit', methods=['get', 'post'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.update_post(post)
        return redirect(url_for('admin.index'))
    return render_template('admin/create_post.html', form=form, type=1, post_id=post_id)

@post.route('/<int:post_id>/del')
@login_required
def del_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('admin.manager'))

@post.route('/create_category',methods=['post','get'])
@login_required
def create_category():
    form=CategoryForm()
    if form.validate_on_submit():
        form.create_category()
        return redirect(url_for('admin.index'))
    return render_template('admin/create_category.html',form=form)


