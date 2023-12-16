
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
        if len(args['idplate']) != 2 or (len(args['alpha']) != 1 and args['alpha']!='الف') or len(args['serial']) != 3 or len(args['city']) != 2:
            return {'reply':False,'msg':'شماره پلاک صحیح نیست '}
        res = self.rules_models.set_rules(args['id'], args['idplate'], args['alpha'], args['serial'], args['city'], args['status'])

        if res:
            return {'reply':True}
        else:
            return {'reply':True, 'msg':'خطا در ثبت'}
        
        
        
