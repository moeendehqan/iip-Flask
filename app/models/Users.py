from pymongo import MongoClient
import datetime
from bson import ObjectId
client = MongoClient()
db = client["iip"]
cl = db['users']

class Users():
    def create_super_user(self):
        if cl.find_one({'username':'admin'}) == None:
            dic = {'username':'admin','password':'admin','creator':'system','date':datetime.datetime.now(),'access':['addconnetion','delrules','getconnetion','delconnetion','concamera','setrules','getrules']}
            cl.insert_one(dic)
        return True
    
    def get_user(self,username,password):
        return cl.find_one({'username':username,'password':password})
    
    def check_cookie(self, id):
        return cl.find_one({'_id':ObjectId(id)})

    def create_user(self,creator,username,password):
        pass


    

    
