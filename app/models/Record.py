from pymongo import MongoClient
import datetime
from bson import ObjectId
import time
client = MongoClient()
db = client["iip"]
cl = db['Record']


class Record():
    def set_record(self, ip, port, type, connect, error, image, plate):
        dic = {'connect':connect,' error':error, 'timestamp':time.time(), "datetime":datetime.datetime.now(), 'ip':ip, 'port':port, 'type':type, 'image':image, 'plate':plate}
        return cl.insert_one(dic)
