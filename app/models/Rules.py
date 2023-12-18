from pymongo import MongoClient
import datetime
from bson import ObjectId

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
        return cl.find({})
    
    def del_rule_by_id(self,_id):
        print(_id)
        cl.delete_one({'_id':ObjectId(_id)})
    
    def get_statuse_by_plate(self,idplate, alpha, serial, city):
        res = cl.find_one({'idplate':idplate, 'alpha':alpha, 'serial':serial, 'city':city})
        if res == None:
            return 0
        if res['status']:
            return 2
        else:
            return 1

        