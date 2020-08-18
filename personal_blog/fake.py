import random

from faker import Faker
from personal_blog.models import Post, Admin, Category
from personal_blog import db

fake = Faker(locale='zh_CN')


def fake_category():
    category = Category(name='编程')
    db.session.add(category)
    db.session.commit()
    category = Category(name='individual_resume')
    db.session.add(category)
    db.session.commit()
    category = Category(name='this_site')
    db.session.add(category)
    db.session.commit()
    category = Category(name='life')
    db.session.add(category)
    db.session.commit()


def fake_posts(count=30):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(800),
            category=Category.query.first(),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(post)
    db.session.commit()


def fake_admin():
    admin = Admin(
        username='admin',
    )
    admin.set_password('flask')

    db.session.add(admin)
    db.session.commit()

