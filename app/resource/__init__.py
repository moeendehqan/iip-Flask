from flask_restful import Api
from .login import Login
from .cookie import Cookie
from .addconnection import AddConnetion
from .getconnection import GetConnetion

api = Api()

api.add_resource(Login, '/login')
api.add_resource(Cookie, '/cookie')
api.add_resource(AddConnetion, '/addconnetion')
api.add_resource(GetConnetion, '/getconnetion')
