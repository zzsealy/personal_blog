from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, ValidationError
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from personal_blog.models import Category


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])

    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


class AdminForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('登陆')


class SetPasswordform(FlaskForm):
    username = StringField('账号', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('提交修改')


class CategoryForm(FlaskForm):
    name = StringField('分类名称', validators=[DataRequired(), Length(1,30)])
    submit = SubmitField('创建')

    def validata_name(self, field):
        if Category.query.fileter_by(name=field.data).first():
            raise ValidationError('分类名称已经存在')
