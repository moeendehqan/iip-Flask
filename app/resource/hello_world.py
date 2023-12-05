from flask_restful import Resource, reqparse



class HelloWorld(Resource):
    def get(self):
        return 'hello world'