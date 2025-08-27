from flask_restx import Namespace, Resource, fields
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db

ns = Namespace('Session', description='会话管理（登录/退出）')

login_model = ns.model('LoginModel', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码')
})

user_info_model = ns.model('UserInfo', {
    'id': fields.Integer(),
    'username': fields.String()
})

@ns.route('/login')
class Login(Resource):
    @ns.expect(login_model, validate=True)
    @ns.marshal_with(user_info_model)
    def post(self):
        """用户登录"""
        data = ns.payload
        user = User.query.filter_by(username=data['username']).first()
        if user and user.verify_password(data['password']):
            login_user(user, remember=True) # 使用 flask_login 登录用户
            return user
        ns.abort(401, '用户名或密码错误')

@ns.route('/logout')
class Logout(Resource):
    @login_required
    def post(self):
        """用户退出"""
        logout_user()
        return {'message': '退出成功'}, 200

@ns.route('/status')
class Status(Resource):
    @login_required
    @ns.marshal_with(user_info_model)
    def get(self):
        """获取当前登录状态"""
        return current_user
