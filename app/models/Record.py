from pymongo import MongoClient
import datetime

import time
client = MongoClient()
db = client["iip"]
cl = db['Record']


class Record():
    def set_record(self,id_camera, ip, port, type, connect, error, image, plate, status):
        current_time = datetime.datetime.now()
        one_minute_ago = current_time - datetime.timedelta(seconds=20)
        dic = {'id_comera':id_camera, 'connect':connect,' error':error, 'timestamp':time.time()*1000, "datetime":current_time, 'ip':ip, 'port':port, 'type':type, 'image':image, 'plate':plate, 'status':status}
        cl.delete_many({'id_comera':id_camera, 'datetime': {'$lt': one_minute_ago}})

        return cl.insert_one(dic)
    
    def get_last_frame_record(self,id_camera):
        res = cl.find_one({'id_comera':id_camera},sort=[('timestamp', -1)])
        return res

