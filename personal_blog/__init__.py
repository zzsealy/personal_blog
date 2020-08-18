from flask import Flask, request, render_template
import os
import logging
from logging.handlers import RotatingFileHandler
from personal_blog.extensions import db, bootstrap, login_manager, ckeditor, csrf, moment, migrate
from personal_blog.blueprints.admin import admin_bp
from personal_blog.blueprints.blog import blog_bp
import click
from personal_blog.fake import fake_posts, fake_admin, fake_category
from personal_blog.models import Post, Admin
from os import urandom
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
    app = Flask('personal_blog')
    config_app(app)
    register_extension(app)
    register_blueprint(app)
    register_faker_value(app)
    register_shell_context(app)
    register_template_context(app)
    register_logger(app)
    return app


def config_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:////' +
                                                      os.path.join(app.root_path, 'data.db'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    key = urandom(10)
    app.secret_key = key
    app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True  # 这个设为True 才能开启代码高亮
    app.config['CKEDITOR_SERVE_LOCAL'] = True


def register_blueprint(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)


# 注册日志
def register_logger(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/personal_blog.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)


# 初始化扩展
def register_extension(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app, db)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(Post=Post, Admin=Admin)


# 注册模版上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        posts = Post.query.order_by(Post.timestamp.desc()).all()

        return dict(
            posts=posts,
            admin=Admin
        )


login_manager.login_view = 'admin.login'
# login_manager.login_message = 'Your custom message'
login_manager.login_message_category = 'warning'


def register_faker_value(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def forge():
        """
        click.echo('创建虚拟文章类型')
        fake_category()
        click.echo('创建虚拟文章')
        fake_posts()
        """
        click.echo('创建管理员')
        fake_admin()
