from flask import Blueprint, render_template, request, flash, current_app
from personal_blog.models import Post, Category
blog_bp = Blueprint('blog', __name__)


# .filter(Post.category.name != 'this_site', Post.category.name != 'individual_resume')
@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # 从查询字符串中获取当前页数
    cate1 = Category.query.filter_by(name='this_site').first()    # 网站介绍的分类。
    cate2 = Category.query.filter_by(name='individual_resume').first()  # 个人简介的分类。
    cate3 = Category.query.filter_by(name='life').first()           # 文字的分类，起的名称是life。
    per_page = 5    # 每页的数量
    pagination = Post.query.filter(Post.category != cate1, Post.category != cate2, Post.category != cate3).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page) # 分页对象
    posts = pagination.items    # 当前页数记录的列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/life')
def index_life():
    page = request.args.get('page', 1, type=int)  # 从查询字符串中获取当前页数
    cate = Category.query.filter_by(name='life').first()
    per_page = 5  # 每页的数量
    pagination = Post.query.filter(Post.category == cate).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  # 分页对象
    posts = pagination.items  # 当前页数记录的列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)




@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.filter().get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)

    return render_template('blog/post.html', post=post, pagination=pagination)


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/individual_resume')
def individual_resume():
    cate = Category.query.filter_by(name='individual_resume').first()
    post = Post.query.filter_by(category=cate).first()
    return render_template('blog/individual_resume.html', post=post)


@blog_bp.route('/this_site')
def this_site():
    cate = Category.query.filter_by(name='this_site').first()
    post = Post.query.filter_by(category=cate).first()
    return render_template('blog/this_site.html', post=post)













