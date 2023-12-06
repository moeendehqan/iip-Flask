from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Connection import Connection
import pandas as pd
from app.service.date import dateProject
from app.service.camera import Camera

parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)


class GetConnetion(Resource):
    def __init__(self):
        self.user_models = Users()
        self.connection_models = Connection()
        self.date_models = dateProject()
        self.camera_models = Camera()


    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "getconnetion" not in user['access']:
            return {'reply':False,'msg':'اجازه دریافت لیست اتصالات را ندارید'}
        df = pd.DataFrame(self.connection_models.get_all_connection())
        df['_id'] = df['_id'].apply(str)
        df['datetime'] = [self.date_models.datetime_to_jalali_str(x) for x in df['datetime']]
        df = df.to_dict('records')
        return {'reply':True,'df':df}