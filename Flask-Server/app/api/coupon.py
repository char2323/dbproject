from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from ..models import Coupon
from .. import db

ns = Namespace('Coupon', description='优惠券相关操作')

coupon_model = ns.model('CouponModel', {
    'id': fields.Integer(),
    'name': fields.String(),
    'discount': fields.Float(),
    'min_spend': fields.Float(),
    'expiry_date': fields.Date(),
    'is_used': fields.Boolean()
})

@ns.route('/')
class CouponList(Resource):
    @login_required
    @ns.marshal_list_with(coupon_model)
    def get(self):
        """获取当前用户的所有优惠券"""
        return current_user.coupons.filter_by(is_used=False).all()
