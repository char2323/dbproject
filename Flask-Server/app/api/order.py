import uuid
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from ..models import Order, Screen, User
from .. import db

ns = Namespace('Order', description='订单相关操作')

# 定义用于订单详情展示的嵌套模型
screen_nested_model = ns.model('ScreenNested', {
    'start_time': fields.DateTime(),
    'cinema_name': fields.String(),
    'hall_name': fields.String()
})
movie_nested_model = ns.model('MovieNested', {
    'name': fields.String(),
    'cover': fields.String()
})
order_detail_model = ns.model('OrderDetailModel', {
    'id': fields.Integer(),
    'order_number': fields.String(),
    'seats': fields.String(),
    'total_price': fields.Float(),
    'status': fields.Integer(description='0:待支付, 1:已支付/待观影, 2:已完成, 3:已取消'),
    'create_time': fields.DateTime(),
    'screen': fields.Nested(screen_nested_model),
    'movie': fields.Nested(movie_nested_model, attribute='screen.movie')
})

# 定义用于创建订单的输入数据模型
order_create_model = ns.model('OrderCreateModel', {
    'screen_id': fields.Integer(required=True, description='场次ID'),
    'seats': fields.String(required=True, description='例如: "5排3座,5排4座"'),
    'total_price': fields.Float(required=True, description='订单总价')
})

@ns.route('/')
class OrderList(Resource):
    @login_required
    @ns.doc('list_user_orders')
    @ns.marshal_list_with(order_detail_model)
    def get(self):
        """获取当前用户的所有订单"""
        return current_user.orders.order_by(Order.create_time.desc()).all()

    @login_required
    @ns.doc('create_new_order')
    @ns.expect(order_create_model, validate=True)
    @ns.marshal_with(order_detail_model, code=201)
    def post(self):
        """为当前用户创建新订单"""
        data = ns.payload
        screen = db.session.get(Screen, data['screen_id'])
        if not screen:
            ns.abort(404, '场次不存在')
        
        new_order = Order(
            order_number=str(uuid.uuid4()),
            user_id=current_user.id,
            screen_id=screen.id,
            seats=data['seats'],
            total_price=data['total_price'],
            status=1 # 简化流程，直接标记为已支付/待观影
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order, 201
