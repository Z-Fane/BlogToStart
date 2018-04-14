from flask_restful import Resource, fields, marshal_with, abort

from app.restful import parsers
from app.models import Post, db, Author
from app.restful.parsers import post_get_parser

post_fields={
    "author": fields.String(attribute=lambda x:x.author.username),
    'title':fields.String(),
    'content':fields.String(),
    'create_time':fields.String()
}
class PostApi(Resource):
    @marshal_with(post_fields)
    def get(self,post_id=None):
        if post_id:
            post=Post.query.filter_by(id=post_id).first()
            return post
        else:
            args=post_get_parser.parse_args()
            page=args['page'] or 1
            posts=Post.query.paginate(page,2)
            return  posts.items

    def post(self,post_id=None):
        if post_id:
            abort(403)
        else:
            args= parsers.post_post_parser.parse_args(strict=True)
            user=Author.verify_auth_token(args['token'])
            if not user:
                abort(401)
            new_post=Post()
            new_post.title=args['title']
            new_post.content=args['content']
            new_post.author=user
            db.session.add(new_post)
            db.session.commit()
            return (new_post.id,201)
    def put(self,post_id=None):
        if not post_id:
            abort(400)
        post=Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404)
        args=parsers.post_put_parser.parse_args()
        user=Author.verify_auth_token(args['token'])
        if not user:
            abort(401)
        if user!=post.author:
            abort(403)
        if args['title']:
            post.title=args['title']
        if args['content']:
            post.content=args['content']
        db.session.add(post)
        db.session.commit()
        return (post.id,201)

    def delete(self,post_id=None):
        if not post_id:
            abort(400)
        post=Post.query.filter_by(id=post_id).first()
        if not post:
            abort(404)
        args = parsers.post_delete_parser.parse_args()
        user = Author.verify_auth_token(args['token'])
        if user!=post.author:
            abort(400)
        db.session.delete(post)
        db.session.commit()
        return ("删除成功",204)



