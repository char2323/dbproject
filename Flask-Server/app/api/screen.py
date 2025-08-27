from flask_restx import Namespace, Resource, fields
from ..models import Screen, Movie
from .. import db

ns = Namespace('Screen', description='场次相关操作')

movie_nested_model = ns.model('MovieNestedForScreen', {
    'name': fields.String(readonly=True, description='电影名称')
})

screen_model = ns.model('ScreenModel', {
    'id': fields.Integer(readonly=True, description='场次唯一ID'),
    'cinema_name': fields.String(required=True, description='影院名称'),
    'hall_name': fields.String(required=True, description='影厅名称'),
    'start_time': fields.DateTime(required=True, description='开始时间'),
    'price': fields.Float(required=True, description='价格'),
    'movie': fields.Nested(movie_nested_model, description='关联的电影信息')
})

@ns.route('/movie/<int:movie_id>')
@ns.param('movie_id', '电影ID')
class ScreensByMovie(Resource):
    @ns.doc('list_screens_by_movie')
    @ns.marshal_list_with(screen_model)
    def get(self, movie_id):
        """根据电影ID获取所有场次列表"""
        movie = db.session.get(Movie, movie_id)
        if not movie:
            ns.abort(404, '电影未找到')
        return movie.screens.order_by(Screen.start_time.asc()).all()

@ns.route('/<int:id>')
@ns.param('id', '场次ID')
class ScreenResource(Resource):
    @ns.doc('get_screen_by_id')
    @ns.marshal_with(screen_model)
    def get(self, id):
        """根据ID获取单个场次详情"""
        screen = db.session.get(Screen, id)
        if not screen:
            ns.abort(404, '场次未找到')
        return screen

@ns.route('/<int:id>/seats')
@ns.param('id', '场次ID')
class ScreenSeats(Resource):
    @ns.doc('get_seat_layout')
    def get(self, id):
        """获取指定场次的座位图"""
        screen = db.session.get(Screen, id)
        if not screen or not screen.seat_layout:
            default_layout = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
            return {'seat_layout': default_layout}
        return {'seat_layout': screen.seat_layout}
