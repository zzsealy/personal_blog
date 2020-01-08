import random

from faker import Faker
from personal_blog.models import Post, User, Category
from personal_blog import db

fake = Faker(locale='zh_CN')


def fake_category():
    category1 = Category(name='编程')
    category2 = Category(name='individual_resume')
    category3 = Category(name='this_site')
    category4 = Category(name='life')
    db.session.add_all([category1, category2, category3,category4])
    db.session.commit()

def fake_user():
    user = User(
        nickname='user',
        password='flask',
    )

    db.session.add(user)
    db.session.commit()

