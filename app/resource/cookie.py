from flask_restful import Resource, reqparse
from app.models.Users import Users


cookie_parser = reqparse.RequestParser()
cookie_parser.add_argument('id', type=str, help='نام کاربری را وارد کنید',required=True)

class Cookie(Resource):
    def __init__(self):
        self.user_models = Users()

    def post(self):
        args = cookie_parser.parse_args()
        if len(args['id'])==0:
            return False
        user = self.user_models.check_cookie(args['id'])

        if user == None:
            return False
        return True