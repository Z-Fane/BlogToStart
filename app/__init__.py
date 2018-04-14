from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_pagedown import PageDown
from flask_restful import Api
from flask_wtf import CSRFProtect

from app.models import db, Author
from app.restful.auth import AuthApi
from app.restful.posts import PostApi
from config import configs
from bs4 import BeautifulSoup as bs

pagedown=PageDown()

def prettify(html):
    soup = bs(html, 'html.parser')
    return soup.prettify()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_restful(app)
    register_extensions(app)
    register_blueprints(app)
    return app
def register_restful(app):
    restful_api=Api()
    restful_api.add_resource(
        PostApi,
        '/api/posts',
        '/api/posts/<string:post_id>',
        endpoint='restful_api_post'
    )
    restful_api.add_resource(
        AuthApi,
        '/api/auth',
        endpoint='restful_api_auth'
    )
    restful_api.init_app(app)
    pass
def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    app.jinja_env.filters['prettify'] = prettify
    pagedown.init_app(app)
    login_manager=LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return Author.query.get(id)
    login_manager.login_view='admin.login'

def register_blueprints(app):
    from .main import admin,login,post,home
    app.register_blueprint(login)
    app.register_blueprint(home)
    app.register_blueprint(admin)
    app.register_blueprint(post)



from app import models

