from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Connection import Connection



parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('_id', type=str, help='اتصال مشخص نیست',required=True)


class DelConnection(Resource):
    def __init__(self):
        self.user_models = Users()
        self.connection_models = Connection()
    
    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "delconnetion" not in user['access']:
            return {'reply':False,'msg':'اجازه حذف اتصالات را ندارید'}
        print(args)
        
        return True