from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from config import Config

# 创建扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
# 如果未认证用户尝试访问受保护页面，
# flask_login 会显示一条消息并重定向。我们这里不需要重定向 URL，
# 因为后台管理面板会处理，但仍然需要配置 login_manager。
login_manager.login_view = "api.Session_login"  # 在某些上下文中仍然有用


def create_app():
    """
    应用工厂函数
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 使用 app 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app, origins="http://localhost:5173", supports_credentials=True)

    # 导入并注册蓝图
    from .api import api_bp as api_blueprint

    app.register_blueprint(api_blueprint)

    # 导入并初始化 Flask-Admin
    from .admin import admin

    admin.init_app(app)

    return app


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login 必需的回调函数。根据 user_id 从数据库加载用户。
    """
    from .models import User

    # 使用 db.session.get 通过主键查找
    return db.session.get(User, int(user_id))
