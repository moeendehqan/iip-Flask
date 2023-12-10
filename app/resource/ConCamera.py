from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Connection import Connection
from app.models.Record import Record
import cv2
import time
import base64
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('_id', type=str, help='شناسه یافت نشد',required=True)


class ConCamera(Resource):
    def __init__(self):
        self.user_models = Users()
        self.connection_models = Connection()
        self.record_models = Record()


    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "concamera" not in user['access']:
            return {'reply':False,'msg':'اجازه اتصال را ندارید '}
        frame = self.record_models.get_last_frame_record(args['_id'])
        frame['datetime'] = str(frame['datetime'])
        frame['_id'] = str(frame['_id'])
        print('1'*23)
        print(frame)

        return {'reply': True, 'frame': frame}


