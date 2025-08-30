from flask_restx import Namespace, Resource, fields
from ..models import Movie
from .. import db

# 创建命名空间，用于电影相关操作
ns = Namespace("Movie", description="电影相关操作")

# 定义电影数据模型
movie_model = ns.model(
    "MovieModel",
    {
        "id": fields.Integer(),  # 电影ID
        "name": fields.String(),  # 电影名称
        "cover": fields.String(),  # 封面图片链接
        "description": fields.String(),  # 电影简介
        "release_date": fields.Date(),  # 上映日期
        "duration_mins": fields.Integer(),  # 电影时长（分钟）
    },
)


@ns.route("/")
class MovieList(Resource):
    @ns.marshal_list_with(movie_model)  # 返回的列表数据按 movie_model 模型序列化
    def get(self):
        """获取电影列表"""
        return Movie.query.all()  # 查询所有电影记录


@ns.route("/<int:id>")
@ns.param("id", "电影ID")  # 为接口文档添加参数说明
class MovieResource(Resource):
    @ns.marshal_with(movie_model)  # 返回的数据按 movie_model 模型序列化
    def get(self, id):
        """获取电影详情"""
        movie = db.session.get(Movie, id)  # 根据主键查询电影
        if not movie:
            ns.abort(404, "电影未找到")  # 如果电影不存在，返回 404
        return movie  # 返回电影信息
