from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import current_user
from wtforms.fields import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import User, Movie, Screen, Order, Comment, Favorite, Coupon
from . import db

# 认证基类（保持不变）
class AuthModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        return "<h1>403 Forbidden</h1>", 403

# 用户视图（保持不变）
class UserAdminView(AuthModelView):
    column_exclude_list = ['password_hash']
    form_excluded_columns = ['password_hash']
    column_searchable_list = ['username', 'phone']
    column_filters = ['create_time']

# 电影查询工厂，用于为下拉框提供选项
def movie_query_factory():
    return Movie.query

# 场次管理视图（关键修改）
class ScreenAdminView(AuthModelView):
    column_list = ('movie', 'cinema_name', 'hall_name', 'start_time', 'price')
    
    # 使用 form_overrides 来自定义表单字段
    form_overrides = {
        'movie': QuerySelectField
    }
    
    # 为自定义的 movie 字段提供参数
    form_args = {
        'movie': {
            'label': 'Movie', # 字段标签
            'query_factory': movie_query_factory, # 指定如何查询选项
            'allow_blank': False # 不允许为空
        }
    }

# 初始化 Admin 实例（保持不变）
admin = Admin(name='猿眼电影后台管理', template_mode='bootstrap4')

# 注册所有视图
admin.add_view(UserAdminView(User, db.session, name='用户管理'))
admin.add_view(AuthModelView(Movie, db.session, name='电影管理'))
admin.add_view(ScreenAdminView(Screen, db.session, name='场次管理'))
admin.add_view(AuthModelView(Order, db.session, name='订单管理'))
admin.add_view(AuthModelView(Comment, db.session, name='评论管理'))
admin.add_view(AuthModelView(Favorite, db.session, name='收藏管理'))
admin.add_view(AuthModelView(Coupon, db.session, name='优惠券管理'))
