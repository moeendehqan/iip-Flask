from pymongo import MongoClient
import datetime
from bson import ObjectId
import time
import pandas as pd
client = MongoClient()
db = client["iip"]
cl = db['Rules']



class Rulse():
    def set_rules(self,creator, type, selectDevice, idplate, alpha, serial, city, status, pinout, duration):
        duplicate = cl.find_one({'idplate':idplate,'alpha':alpha,'serial':serial,'city':city})
        if duplicate != None:
            return False
        cl.insert_one({'creator':creator, 'type':type, 'selectDevice':selectDevice, 'idplate':idplate,'alpha':alpha,'serial':serial,'city':city, 'status':status,'pinout':pinout, 'duration':duration, "datetime":datetime.datetime.now()})
        return True
    
    def get_all_rules(self):
        return cl.find({})
    
    def get_id_camera_object(self):
        res = cl.find({'type':'Object'})
        res = [x['selectDevice'] for x in res]
        return res
