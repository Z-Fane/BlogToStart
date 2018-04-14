from flask import current_app, abort
from flask_restful import Resource
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import Author
from app.restful import parsers


class AuthApi(Resource):
    def post(self):
        args=parsers.user_post_parser.parse_args()
        user=Author.query.filter_by(username=args['username']).first()
        if user.check_password(args['password']):
            serializer=Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=6000000
            )
            jsonstr=serializer.dumps({'id': user.id})
            return {'token':jsonstr.decode()}
        else:
            abort(404)