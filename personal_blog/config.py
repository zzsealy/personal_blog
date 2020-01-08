import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '' 
    FLASKY_MAIL_SENDER = 'zzsealy'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    ADMIN = os.environ.get('ADMIN')
    CKEDITOR_ENABLE_CODESNIPPET = True
    CKEDITOR_SERVE_LOCAL = True
    PER_PAGE=15
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:////' + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE=8
    @staticmethod
    def init_app(app):
        pass


config = Config()
