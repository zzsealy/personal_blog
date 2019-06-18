from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from flask_moment import Moment
from flask_migrate import Migrate

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
moment = Moment()
migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from personal_blog.models import Admin     # 在这里导入为了防止循环依赖
    user = Admin.query.get(int(user_id))
    return user

