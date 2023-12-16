from pymongo import MongoClient
import datetime
from bson import ObjectId
import pandas as pd
import time
from app.service.date import dateProject

client = MongoClient()
db = client["iip"]
cl = db['Rules']



class Rulse():
    def set_rules(self,creator, idplate, alpha, serial, city, status):
        duplicate = cl.find_one({'idplate':idplate,'alpha':alpha,'serial':serial,'city':city})
        if duplicate != None:
            return False
        cl.insert_one({'creator':creator,'idplate':idplate,'alpha':alpha,'serial':serial,'city':city, 'status':status, "datetime":datetime.datetime.now()})
        return True
    def get_all_rules(self):
        df = pd.DataFrame(cl.find({}))
        dp = dateProject()
        df['_id'] = df['_id'].apply(str)
        df['datetime'] = df['datetime'].apply(dp.datetime_to_jalali_str)
        df['plate'] = df['idplate'] + df['alpha'] + df['serial']  + df['city']
        df = df.to_dict('records')
        return df
    def del_rule_by_id(self,_id):
        cl.delete_one({'_id':ObjectId(_id)})
        return True
    def get_by_num(self, idplate, alpha, serial, city):
        return cl.find_one({'plate':{'idplate':idplate, 'alpha':alpha, 'serial':serial, 'city':city}})