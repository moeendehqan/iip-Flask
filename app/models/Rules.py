from pymongo import MongoClient
import datetime
from bson import ObjectId
import time
client = MongoClient()
db = client["iip"]
cl = db['Rules']



class Rulse():
    def set_rules(self,creator, idplate, alpha, serial, city, status):
        duplicate = cl.find({'idplate':idplate,'alpha':alpha,'serial':serial,'city':city}) != None
        if duplicate:
            return False
        cl.insert_one({'creator':creator,'idplate':idplate,'alpha':alpha,'serial':serial,'city':city, 'status':status, "datetime":datetime.datetime.now()})
        return True
    def get_all_rules(self):
        res = cl.find({})
        return [x for x in res]