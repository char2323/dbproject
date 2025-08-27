from flask_restx import Namespace, Resource, fields
from ..models import Movie
from .. import db

ns = Namespace('Movie', description='电影相关操作')

movie_model = ns.model('MovieModel', {
    'id': fields.Integer(),
    'name': fields.String(),
    'cover': fields.String(),
    'description': fields.String(),
    'release_date': fields.Date(),
    'duration_mins': fields.Integer()
})

@ns.route('/')
class MovieList(Resource):
    @ns.marshal_list_with(movie_model)
    def get(self):
        """获取电影列表"""
        return Movie.query.all()

@ns.route('/<int:id>')
@ns.param('id', '电影ID')
class MovieResource(Resource):
    @ns.marshal_with(movie_model)
    def get(self, id):
        """获取电影详情"""
        movie = db.session.get(Movie, id)
        if not movie:
            ns.abort(404, '电影未找到')
        return movie
