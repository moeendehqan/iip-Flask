
from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Rules import Rulse


parser = reqparse.RequestParser()

parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('idplate', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('alpha', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('serial', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('city', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('status', type=bool, help='نام id را وارد کنید',required=True)


class SetRules(Resource):
    def __init__(self):
        self.user_models = Users()
        self.rules_models = Rulse()

    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "setrules" not in user['access']:
            return {'reply':False,'msg':'اجازه افزودن قانون را ندارید '}
        res = self.
        
        
