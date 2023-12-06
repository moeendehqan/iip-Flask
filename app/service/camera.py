import cv2
from app.models.Connection import Connection


class Camera():
    def __init__(self):
        self.connetion_model = Connection()
    def check_connect_rtps_by_id(self,id_connection):
        connection = self.connetion_model.get_connection_by_id(id_connection)
        if connection == None:
            return False
        ip_address = connection['ip']
        port = connection['port']
        username = connection['username']
        password = connection['password']
        rtsp_url = f'rtsp://{username}:{password}@{ip_address}:{port}/Streaming/Channels/101'
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            return False
        ret, frame = cap.read()
        if not ret:
            return False
        return True



