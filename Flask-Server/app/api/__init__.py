from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__, url_prefix='/api')

api = Api(api_bp, version='1.0', title='MonkeyEye API', description='猿眼电影订票系统 API', doc='/swagger/')

# 导入并注册所有命名空间 (Namespace)
from .user import ns as user_ns
from .session import ns as session_ns
from .movie import ns as movie_ns
from .screen import ns as screen_ns
from .order import ns as order_ns
from .comment import ns as comment_ns
from .favorite import ns as favorite_ns
from .coupon import ns as coupon_ns

api.add_namespace(user_ns, path='/users')
api.add_namespace(session_ns, path='/session')
api.add_namespace(movie_ns, path='/movies')
api.add_namespace(screen_ns, path='/screens')
api.add_namespace(order_ns, path='/orders')
api.add_namespace(comment_ns, path='/comments')
api.add_namespace(favorite_ns, path='/favorites')
api.add_namespace(coupon_ns, path='/coupons')
