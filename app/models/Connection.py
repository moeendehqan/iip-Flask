from pymongo import MongoClient
import datetime
from bson import ObjectId
client = MongoClient()
db = client["iip"]
cl = db['connection']


class Connection():
    def get_connection_by_ip(self,ip):
        return cl.find_one({'ip':ip})
    
    def get_connection_by_name(self,name):
        return cl.find_one({'name':name})
    
    def get_connection_by_id(self,id):
        return cl.find_one({'_id':ObjectId(id)})
    
    def create_connection(self, name, ip, port, username, password, creator):
        cl.insert_one({'name':name, 'ip':ip, 'port':port, 'username':username, "password":password, 'creator':creator, 'datetime':datetime.datetime.now()})
        return True
    
    def get_all_connection(self):
        return cl.find()
    
    def del_connectionn_by_id(self,id):
        cl.delete_one({'_id':ObjectId(id)})
        return True
        