from flask_restful import Resource, reqparse
from app.models.Users import Users

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, help='نام کاربری را وارد کنید',required=True)
login_parser.add_argument('password', type=str, help='رمزعبور را وارد کنید',required=True)

class Login(Resource):
    def __init__(self):
        self.user_models = Users()

    def post(self):
        args = login_parser.parse_args()
        user = self.user_models.get_user(args['username'],args['password'])
        if user == None:
            return {'reply':False,'msg':'نام کاربری یا رمز عبور صحیح نیست'}
        return {'reply':True,'id':str(user['_id'])}
