from flask import Blueprint, render_template, url_for, redirect, flash, request
from personal_blog.models import Admin, Post, Category
from flask_login import login_user, logout_user, login_required, current_user
from personal_blog.form import LoginForm, PostForm, AdminForm, SetPasswordform, CategoryForm
from personal_blog.setting import redirect_back
from personal_blog.extensions import db

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(u'你已经登陆了！', 'info')
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and password == admin.password:
                login_user(admin, remember)
                flash('登陆成功', 'info')
                return redirect_back()

            flash('账号密码错误', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'退出登录', 'info')
    return redirect_back()


@admin_bp.route('/setting')
@login_required   # 视图保护，只有登陆了才能看到这个被这个装饰器修饰的路由
def setting():
    return render_template('admin/setting.html')


@admin_bp.route('/category/manage')
@login_required
def manage_category():
    categories = Category.query.all()
    return render_template('admin/manage_category.html', categories=categories)


@admin_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash('分类创建成功！', 'success')
        return redirect(url_for('.manage_category'))
    return render_template('admin/new_category.html', form=form)


@admin_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('你不能修改默认的分类', 'warning')
        return redirect('blog.index')
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('文章分类更新成功')
        return redirect(url_for('.manage_category'))
    form.name.data = category.name
    return render_template('/admin/edit_category.html', form=form)


@admin_bp.route('/category<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('你不能删除默认的分类', 'warning')
        return redirect('blog.index')
    category.delete()
    flash('分类删除成功')
    return redirect(url_for('.manage_category'))


@admin_bp.route('/manage_post')   # 文章管理
@login_required
def manage():
    page = request.args.get('page', 1, type=int)  # 从查询字符串中获取当前页数
    per_page = 5  # 每页的数量
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)  # 分页对象
    posts = pagination.items  # 当前页数记录的列表

    return render_template('admin/manage_post.html', pagination=pagination, posts=posts)


@admin_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = Category.query.get(form.category.data)
        post.body = form.body.data
        db.session.commit()
        flash('文章更新成功')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.category.data = post.category_id
    form.body.data = post.body
    return render_template('/admin/edit_post.html', form=form)


@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章删除成功！')
    return redirect_back()


@admin_bp.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, category=category, body=body)
        db.session.add(post)
        db.session.commit()
        flash('博客发表成功')
        return redirect(url_for('blog.index'))
    return render_template('/admin/new_post.html', form=form)


# 修改个人简介
@admin_bp.route('/edit_individual_resume',  methods=['GET', 'POST'])
def edit_indicidual_resume():
    cate = Category.query.filter_by(name='individual_resume').first()
    post = Post.query.filter_by(category=cate).first()
    return redirect(url_for('admin.edit_post', post_id=post.id))


# 修改网站介绍
@admin_bp.route('/edit_this_site', methods=['GET', 'POST'])
def edit_this_site():
    cate = Category.query.filter_by(name='this_site').first()
    post = Post.query.filter_by(category=cate).first()
    return redirect(url_for('admin.edit_post', post_id=post.id))


@admin_bp.route('/set_password', methods=['GET', 'POST'])
@login_required
def set_password():
    form = SetPasswordform()
    if form.validate_on_submit():
        admin = Admin.query.first()
        admin.username = form.username.data
        admin.password = form.password.data
        db.session.add(admin)
        db.session.commit()
        flash('密码修改成功')
        return redirect(url_for('blog.index'))
    return render_template('/admin/set_password.html', form=form)

