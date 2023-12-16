
from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Rules import Rulse
import pandas as pd
from app.service.date import dateProject
parser = reqparse.RequestParser()

parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)


class GetRules(Resource):
    def __init__(self):
        self.user_models = Users()
        self.rules_models = Rulse()
        self.dateProject_models = dateProject()


    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "getrules" not in user['access']:
            return {'reply':False,'msg':'اجازه مشاهده قانون را ندارید '}
        df = self.rules_models.get_all_rules()
        df = pd.DataFrame(df)
        if len(df) == 0:
            return {'replay':False, 'msg':'خالی است'}
        df['datetime'] = df['datetime'].apply(self.dateProject_models.datetime_to_jalali_str)
        df['_id'] = df['_id'].apply(str)
        df = df.to_dict('records')
        return {'reply':True, 'df':df}