from flask_restful import Api
from .login import Login
from .cookie import Cookie
from .addconnection import AddConnetion
from .getconnection import GetConnetion
from .delconnection import DelConnection
from .ConCamera import ConCamera
from .SetRules import SetRules
from .get

api = Api()

api.add_resource(Login, '/login')
api.add_resource(Cookie, '/cookie')
api.add_resource(AddConnetion, '/addconnetion')
api.add_resource(GetConnetion, '/getconnetion')
api.add_resource(DelConnection, '/delconnection')
api.add_resource(ConCamera, '/concamera')
api.add_resource(SetRules, '/setrules')
api.add_resource(GetRules, '/getrules')
api.add_resource(DelRules, '/delrules')
