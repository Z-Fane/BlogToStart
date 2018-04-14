from flask_restful import reqparse

post_get_parser=reqparse.RequestParser()

post_get_parser.add_argument(
    'page',
    type=int,
    location=['json','args','header'],
    required=False
)
post_post_parser=reqparse.RequestParser()

post_post_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Title is required!'
)
post_post_parser.add_argument(
    'content',
    type=str,
    required=True,
    help='Content is required!'
)
post_post_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Token is required!'
)
user_post_parser=reqparse.RequestParser()
user_post_parser.add_argument('username',type=str,required=True,help='Username is required!')
user_post_parser.add_argument('password',type=str,required=True,help='Password is required!')


post_put_parser=reqparse.RequestParser()
post_put_parser.add_argument(
    'title',
    type=str,
    required=True,
    help='Title is required!'
)
post_put_parser.add_argument(
    'content',
    type=str,
    required=True,
    help='Content is required!'
)
post_put_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Token is required!'
)


post_delete_parser=reqparse.RequestParser()
post_delete_parser.add_argument(
    'token',
    type=str,
    required=True,
    help='Token is required!'
)