from flask_restx import Namespace, Resource, fields
from ..models import Screen, Movie
from .. import db

# 创建命名空间，用于场次相关操作
ns = Namespace("Screen", description="场次相关操作")

# 定义嵌套的电影信息模型，用于场次返回结果中嵌套电影信息
movie_nested_model = ns.model(
    "MovieNestedForScreen",
    {"name": fields.String(readonly=True, description="电影名称")},
)

# 定义场次数据模型
screen_model = ns.model(
    "ScreenModel",
    {
        "id": fields.Integer(readonly=True, description="场次唯一ID"),
        "cinema_name": fields.String(required=True, description="影院名称"),
        "hall_name": fields.String(required=True, description="影厅名称"),
        "start_time": fields.DateTime(required=True, description="开始时间"),
        "price": fields.Float(required=True, description="价格"),
        "movie": fields.Nested(movie_nested_model, description="关联的电影信息"),
    },
)


@ns.route("/movie/<int:movie_id>")
@ns.param("movie_id", "电影ID")
class ScreensByMovie(Resource):
    @ns.doc("list_screens_by_movie")  # API文档标识
    @ns.marshal_list_with(screen_model)  # 返回值序列化为 screen_model 列表
    def get(self, movie_id):
        """根据电影ID获取所有场次列表"""
        movie = db.session.get(Movie, movie_id)  # 根据主键查询电影
        if not movie:
            ns.abort(404, "电影未找到")  # 如果电影不存在，返回 404
        # 返回该电影的所有场次，并按开始时间升序排列
        return movie.screens.order_by(Screen.start_time.asc()).all()


@ns.route("/<int:id>")
@ns.param("id", "场次ID")
class ScreenResource(Resource):
    @ns.doc("get_screen_by_id")  # API文档标识
    @ns.marshal_with(screen_model)  # 返回值序列化为 screen_model
    def get(self, id):
        """根据ID获取单个场次详情"""
        screen = db.session.get(Screen, id)  # 根据主键查询场次
        if not screen:
            ns.abort(404, "场次未找到")  # 如果场次不存在，返回 404
        return screen  # 返回场次信息


@ns.route("/<int:id>/seats")
@ns.param("id", "场次ID")
class ScreenSeats(Resource):
    @ns.doc("get_seat_layout")  # API文档标识
    def get(self, id):
        """获取指定场次的座位图"""
        screen = db.session.get(Screen, id)  # 根据主键查询场次
        # 如果场次不存在或没有座位图，返回默认座位布局
        if not screen or not screen.seat_layout:
            default_layout = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
            return {"seat_layout": default_layout}  # 返回默认座位图
        # 返回实际座位布局
        return {"seat_layout": screen.seat_layout}
