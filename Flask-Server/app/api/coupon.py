from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from ..models import Coupon
from .. import db

# 创建命名空间，用于优惠券相关操作
ns = Namespace("Coupon", description="优惠券相关操作")

# 定义优惠券数据模型
coupon_model = ns.model(
    "CouponModel",
    {
        "id": fields.Integer(),  # 优惠券ID
        "name": fields.String(),  # 优惠券名称
        "discount": fields.Float(),  # 折扣额度
        "min_spend": fields.Float(),  # 使用最低消费金额
        "expiry_date": fields.Date(),  # 到期日期
        "is_used": fields.Boolean(),  # 是否已使用
    },
)


@ns.route("/")
class CouponList(Resource):
    @login_required  # 该接口需要用户登录才能访问
    @ns.marshal_list_with(coupon_model)  # 返回的数据按 coupon_model 模型序列化
    def get(self):
        """获取当前用户的所有未使用优惠券"""
        # 返回当前登录用户所有未使用的优惠券
        return current_user.coupons.filter_by(is_used=False).all()
