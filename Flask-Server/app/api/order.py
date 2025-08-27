import uuid
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from sqlalchemy.orm.attributes import flag_modified
from ..models import Order, Screen, User
from .. import db

ns = Namespace('Order', description='订单相关操作')

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
        """为当前用户创建新订单，并更新座位图"""
        data = ns.payload
        screen_id = data['screen_id']
        seats_str = data['seats']
        
        screen = db.session.get(Screen, screen_id)
        if not screen:
            ns.abort(404, '场次不存在')

        seat_layout = screen.seat_layout
        if not seat_layout:
            ns.abort(500, '该场次未配置座位图')

        selected_seats_list = seats_str.split(',')
        for seat in selected_seats_list:
            try:
                row_str, col_str = seat.replace('排', ' ').replace('座', '').split()
                row_index = int(row_str) - 1
                col_index = int(col_str) - 1

                if seat_layout[row_index][col_index] == 1:
                    ns.abort(409, f"座位 {seat} 已被预定，请重新选择")
                
                seat_layout[row_index][col_index] = 1
            except (ValueError, IndexError):
                ns.abort(400, f"座位格式错误: {seat}")

        flag_modified(screen, "seat_layout")

        new_order = Order(
            order_number=str(uuid.uuid4()),
            user_id=current_user.id,
            screen_id=screen.id,
            seats=data['seats'],
            total_price=data['total_price'],
            status=1
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order, 201
