from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from ..models import Favorite, Movie
from .. import db

ns = Namespace('Favorite', description='收藏/想看/已看')

# 输入模型
favorite_update_model = ns.model('FavoriteUpdateModel', {
    'movie_id': fields.Integer(required=True, description='电影ID'),
    'status': fields.Integer(required=True, description='1:想看, 2:已看')
})

# 输出模型，包含完整的电影信息
movie_nested_model = ns.model('MovieForFavorite', {
    'id': fields.Integer(),
    'name': fields.String(),
    'cover': fields.String()
})
favorite_model = ns.model('FavoriteModel', {
    'movie': fields.Nested(movie_nested_model),
    'status': fields.Integer(description='1:想看, 2:已看')
})

@ns.route('/')
class FavoriteList(Resource):
    @login_required
    @ns.doc('get_user_favorites')
    @ns.marshal_list_with(favorite_model)
    def get(self):
        """获取当前用户所有收藏/想看/已看记录"""
        return current_user.favorites.all()

    @login_required
    @ns.doc('add_or_update_favorite')
    @ns.expect(favorite_update_model, validate=True)
    def post(self):
        """为当前用户添加或更新一条收藏/想看/已看记录"""
        data = ns.payload
        movie_id = data['movie_id']
        status = data['status']

        if not db.session.get(Movie, movie_id):
            ns.abort(404, '电影不存在')

        # 查找是否已存在记录
        fav = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        
        if fav:
            # 如果存在，则更新状态
            fav.status = status
        else:
            # 如果不存在，则创建新记录
            fav = Favorite(user_id=current_user.id, movie_id=movie_id, status=status)
            db.session.add(fav)
        
        db.session.commit()
        return {'message': '操作成功'}, 201

@ns.route('/<int:movie_id>')
@ns.param('movie_id', '电影ID')
class FavoriteItem(Resource):
    @login_required
    @ns.doc('delete_favorite')
    @ns.response(204, '删除成功')
    def delete(self, movie_id):
        """为当前用户删除一条收藏记录"""
        fav = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        
        if fav:
            db.session.delete(fav)
            db.session.commit()
        
        return '', 204

@ns.route('/status/<int:movie_id>')
@ns.param('movie_id', '电影ID')
class FavoriteStatus(Resource):
    @login_required
    @ns.doc('get_favorite_status_for_movie')
    def get(self, movie_id):
        """获取当前用户对某部电影的收藏状态"""
        fav = Favorite.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if fav:
            return {'status': fav.status}
        return {'status': 0} # 0 表示未收藏/想看/已看
