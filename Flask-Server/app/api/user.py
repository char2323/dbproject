from flask_restx import Namespace, Resource, fields
from ..models import User
from .. import db

# 创建用户模块的命名空间
ns = Namespace('User', description='用户相关操作')

# 定义 API 的数据模型 (用于 Swagger 文档和输入/输出验证)
user_model = ns.model('UserModel', {
    'id': fields.Integer(readonly=True, description='用户唯一ID'),
    'username': fields.String(required=True, description='用户名'),
    'phone': fields.String(required=True, description='手机号'),
    'avatar': fields.String(description='头像链接'),
    'create_time': fields.DateTime(description='注册时间')
})

# 用于创建用户的输入模型 (只包含必要的字段)
user_create_model = ns.model('UserCreateModel', {
    'username': fields.String(required=True, description='用户名'),
    'password': fields.String(required=True, description='密码', min_length=6),
    'phone': fields.String(required=True, description='手机号')
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """获取所有用户列表"""
        return User.query.all()

    @ns.doc('create_user')
    @ns.expect(user_create_model, validate=True)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """创建新用户（注册）"""
        data = ns.payload
        if User.query.filter_by(username=data['username']).first():
            ns.abort(409, f"用户名 '{data['username']}' 已存在")
        if User.query.filter_by(phone=data['phone']).first():
            ns.abort(409, f"手机号 '{data['phone']}' 已被注册")
            
        new_user = User(
            username=data['username'],
            password=data['password'], # password setter 会自动处理哈希
            phone=data['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

@ns.route('/<int:id>')
@ns.response(404, '用户未找到')
@ns.param('id', '用户ID')
class UserResource(Resource):
    @ns.doc('get_user')
    @ns.marshal_with(user_model)
    def get(self, id):
        """根据ID获取用户信息"""
        user = db.session.get(User, id)
        if not user:
            ns.abort(404, f"ID为 {id} 的用户不存在")
        return user

