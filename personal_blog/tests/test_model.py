import unittest
from personal_blog import create_app, db
from personal_blog.models import User, AnonymousUser, Role, Permission

class UserModelTestCase(unittest.TestCase):
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()   # 建立角色User类型
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
