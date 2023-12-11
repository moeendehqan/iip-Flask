from pymongo import MongoClient
import datetime
from bson import ObjectId
import time
client = MongoClient()
db = client["iip"]
cl = db['Record']


class Record():
    def set_record(self,id_camera, ip, port, type, connect, error, image, plate):
        current_time = datetime.datetime.now()
        one_minute_ago = current_time - datetime.timedelta(minutes=1)
        dic = {'id_comera':id_camera, 'connect':connect,' error':error, 'timestamp':time.time(), "datetime":datetime.datetime.now(), 'ip':ip, 'port':port, 'type':type, 'image':image, 'plate':plate}
        cl.delete_many({'id_comera':id_camera, 'datetime': {'$lt': one_minute_ago}})
        return cl.insert_one(dic)
    def get_last_frame_record(self,id_camera):
        return cl.find_one({'id_comera':id_camera},sort=[('datetime', -1)])

