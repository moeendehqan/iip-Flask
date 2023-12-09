from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Connection import Connection
import ipaddress

parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('name', type=str, help='نام دستگاه را وارد کنید',required=True)
parser.add_argument('type', type=str, help='نوع دستگاه را وارد کنید',required=True)
parser.add_argument('ip', type=str, help='ip را وارد کنید',required=True)
parser.add_argument('port', type=str, help='port را وارد کنید',required=True)
parser.add_argument('username', type=str, help='نام کاربری را وارد کنید',required=True)
parser.add_argument('password', type=str, help='نام رمزعبور را وارد کنید',required=True)


class AddConnetion(Resource):
    def __init__(self):
        self.user_models = Users()
        self.connection_models = Connection()

    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "addconnetion" not in user['access']:
            return {'reply':False,'msg':'اجازه افزودن اتصال را ندارید '}
        if args['type'] == 'ip':
            try:
                ipaddress.ip_address(args['ip'])
            except:
                return {'reply':False,'msg':'ادرس ip صحیح نیست'}
        if self.connection_models.get_connection_by_ip(args['ip']) and args['type'] == 'ip' != None:
            return {'reply':False,'msg':'ادرس ip تکراری است'}
        if self.connection_models.get_connection_by_name(args['name']) != None:
            return {'reply':False,'msg':'نام دستگاه تکراری است'}
        if not args['port'].isdigit() and args['type'] == 'ip':
            return {'reply':False,'msg':'port صحیح نیست'}
        if int(args['port'])>65535 or int(args['port'])<=0 and args['type'] == 'ip':
            return {'reply':False,'msg':'port صحیح نیست'}
        if len(args['username'])<3 and args['type'] == 'ip':
            return {'reply':False,'msg':'نام کاربری صحیح نیست'}
        if len(args['password'])<3 and args['type'] == 'ip':
            return {'reply':False,'msg':'نام رمزعبور صحیح نیست'}
        self.connection_models.create_connection(args['type'], args['name'], args['ip'], int(args['port']), args['username'], args['password'], args['id'])
        return {'reply':True}