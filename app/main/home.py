from flask import Blueprint, render_template, request, current_app
from sqlalchemy import extract, func

from app.models import Post, Tag, db

home=Blueprint('home',__name__,url_prefix='/')


@home.route('/')
def index():
    page=request.args.get('page',default=1,type=int)
    pagination=Post.query.order_by(Post.create_time.desc()).paginate(page=page,per_page=current_app.config['ADMIN_PER_PAGE'],error_out=False)
    return render_template('home.html', title="Home", pagination=pagination)


@home.route('archive')
def archive():
    post_list={}
    years=db.session.query(func.year(Post.create_time).label('year')).group_by('year').all()
    for x in years:
        post_list[x[0]]=(Post.query.filter(func.year(Post.create_time)==x).all())
    return render_template('archive.html', title='Archive', post_list=post_list)


@home.route('author/<int:author_id>')
def postByAuthor(author_id):
    posts = Post.query.filter_by(author_id=author_id)
    return render_template('archive.html', title='123', posts=posts)


@home.route('tag/<int:tag_id>')
def postByTag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    post_list={}
    # years = db.session.query(func.year(Post.create_time).label('year')).group_by('year').all()
    # for x in years:
    #     post_list[x[0]] = (Post.query.filter(func.year(Post.create_time) == x).all())
    posts=tag.Post.order_by(Post.create_time.desc()).all()

    for post in posts:
        if post_list.get(post.create_time.year) is None:
            post_list[post.create_time.year]=[]
            post_list[post.create_time.year].append(post)
        else:
            post_list[post.create_time.year].append(post)
    return render_template('archive.html', title='321', post_list=post_list)