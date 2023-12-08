from flask_restful import Resource, reqparse
from app.models.Users import Users
from app.models.Connection import Connection
import cv2
import numpy as np
from flask import Flask, Response, jsonify
import base64
parser = reqparse.RequestParser()
parser.add_argument('id', type=str, help='نام id را وارد کنید',required=True)
parser.add_argument('_id', type=str, help='شناسه یافت نشد',required=True)


class ConCamera(Resource):
    def __init__(self):
        self.user_models = Users()
        self.connection_models = Connection()
        self.cap = None

    def open_camera(self, rtsp_url):
        try:
            self.cap = cv2.VideoCapture(rtsp_url)
            if not self.cap.isOpened():
                return False
            return True
        except Exception as e:
            print(f'خطا در اتصال به دوربین: {str(e)}')
            return False

    def close_camera(self):
        if self.cap is not None:
            self.cap.release()

    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                return frame_bytes
        return None

    def post(self):
        args = parser.parse_args()
        user = self.user_models.check_cookie(args['id'])
        if user == None:
            return {'reply':False,'msg':'خطا ناشناخته لطفا مجدد وارد شوید'}
        if "addconnetion" not in user['access']:
            return {'reply':False,'msg':'اجازه افزودن اتصال را ندارید '}
        connection = self.connection_models.get_connection_by_id(args['_id'])
        username = connection['username']
        password = connection['password']
        ip = connection['ip']
        port = connection['port']
        rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=1"

        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            return {'replay':False,'msg':'اتصال برقرار نشد'}
        ret, frame = cap.read() 
        original_height, original_width, _ = frame.shape
        height = int(original_height *0.5)
        width = int(original_width *0.5)
        frame = cv2.resize(frame, (height, width))
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')

        return {'reply': True, 'image': frame_bytes}


    def __del__(self):
        self.close_camera()