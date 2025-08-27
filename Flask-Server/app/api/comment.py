from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from ..models import Comment, Movie, User
from .. import db

ns = Namespace('Comment', description='评论相关操作')

# 用于评论中显示的用户信息
user_nested_model = ns.model('UserForComment', {
    'username': fields.String(readonly=True)
})

# 评论输出模型
comment_model = ns.model('CommentModel', {
    'id': fields.Integer(readonly=True),
    'content': fields.String(),
    'rating': fields.Float(),
    'create_time': fields.DateTime(),
    'user': fields.Nested(user_nested_model) # 包含用户信息
})

# 评论输入模型
comment_create_model = ns.model('CommentCreateModel', {
    'content': fields.String(required=True, description='评论内容'),
    'rating': fields.Float(required=True, description='评分 (1-5)', min=1, max=5)
})

@ns.route('/movie/<int:movie_id>')
@ns.param('movie_id', '电影ID')
class MovieComments(Resource):
    @ns.doc('get_movie_comments')
    @ns.marshal_list_with(comment_model)
    def get(self, movie_id):
        """获取某部电影的所有评论"""
        movie = db.session.get(Movie, movie_id)
        if not movie:
            ns.abort(404, '电影未找到')
        return movie.comments.order_by(Comment.create_time.desc()).all()

    @login_required
    @ns.doc('add_movie_comment')
    @ns.expect(comment_create_model, validate=True)
    @ns.marshal_with(comment_model, code=201)
    def post(self, movie_id):
        """为某部电影添加新评论"""
        if not db.session.get(Movie, movie_id):
            ns.abort(404, '电影未找到')
        
        data = ns.payload
        new_comment = Comment(
            user_id=current_user.id,
            movie_id=movie_id,
            content=data['content'],
            rating=data['rating']
        )
        db.session.add(new_comment)
        db.session.commit()
        return new_comment, 201
