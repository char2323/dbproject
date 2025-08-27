from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.types import JSON # 导入 JSON 类型

# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    avatar = db.Column(db.String(256), default='default_avatar.png')
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self): raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password): self.password_hash = generate_password_hash(password)
    def verify_password(self, password): return check_password_hash(self.password_hash, password)

# 电影表
class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    cover = db.Column(db.String(256))
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    duration_mins = db.Column(db.Integer)

# 场次表
class Screen(db.Model):
    __tablename__ = 'screens'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    cinema_name = db.Column(db.String(128))
    hall_name = db.Column(db.String(64))
    start_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seat_layout = db.Column(JSON) # 新增座位图字段

    movie = db.relationship('Movie', backref=db.backref('screens', lazy='dynamic'))

# 订单表
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    screen_id = db.Column(db.Integer, db.ForeignKey('screens.id'), nullable=False)
    seats = db.Column(db.String(256), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.Integer, default=0, index=True)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('orders', lazy='dynamic'))
    screen = db.relationship('Screen')

# 评论表
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    content = db.Column(db.Text)
    rating = db.Column(db.Float)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    movie = db.relationship('Movie', backref=db.backref('comments', lazy='dynamic'))

# 收藏/想看/已看 记录表
class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    user = db.relationship('User', backref=db.backref('favorites', lazy='dynamic'))
    movie = db.relationship('Movie', backref=db.backref('favorites', lazy='dynamic'))

# 优惠券表
class Coupon(db.Model):
    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(128))
    discount = db.Column(db.Float)
    min_spend = db.Column(db.Float)
    expiry_date = db.Column(db.Date)
    is_used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref=db.backref('coupons', lazy='dynamic'))
