
from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Rules import Rulse





parser = reqparse.RequestParser()

parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('_id', type=str, help='قانون یافت نشد',required=True)


class DelRules(Resource):
    def __init__(self):
        self.user_models = Users()
        self.rules_models = Rulse()

    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "setrules" not in user['access']:
            return {'reply':False,'msg':'اجازه حذف قانون را ندارید'}
        self.rules_models.del_rule_by_id(args['_id'])
        return {'reply':True}