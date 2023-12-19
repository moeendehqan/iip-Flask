from app.models.Record import Record
from app.models.Connection import Connection
from hezar.models import Model
from app.service.RulesHandle import RulesHandle
from app.models.Rules import Rulse
import cv2
import yolov5
import time
import base64
import torch
import os
class CameraHandle():
    def __init__(self):
        self.record_model = Record()
        self.connection_models = Connection()
        self.cap = None
        self.device = "cpu"
        model_path = os.path.join(os.getcwd(), 'app', 'service', 'ml', 'yolov5n-license-plate', 'best.pt')
        self.model = yolov5.load(model_path)
        self.model = self.model.to(self.device)
        self.model.conf = 0.25  # NMS confidence threshold
        self.model.iou = 0.45  # NMS IoU threshold
        self.model.agnostic = False  # NMS class-agnostic
        self.model.multi_label = False  # NMS multiple labels per box
        self.model.max_det = 1000  # maximum number of detections per image
        self.count = 0
        model_path = os.path.join(os.getcwd(), 'app', 'service', 'ml', 'crnn')
        self.model_Ocr = Model.load(
            hub_or_local_path=model_path,
            load_locally=True,
            load_preprocessor=True,
            model_filename='model.pt',
            config_filename='model_config.yaml'
        )
        try:
            self.rule_handle_model = RulesHandle()
        except:
            pass
    
        self.rule_model = Rulse()

    
    def prossece_plate(self, frame,_id, ip, port, type):
        try:
            results = self.model(frame, augment=True)
            predictions = results.pred[0]
            plates = []
            status = 1
            if len(predictions) > 0:
                boxes = predictions[:, :4]
                scores = predictions[:, 4]
                categories = predictions[:, 5]
                for i in range(len(boxes)):
                    x1, y1, x2, y2 = boxes[i]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    score = scores[i]
                    if float(score)>0.40:

                        cropped_image = frame[y1:y2, x1:x2]
                        # تبدیل تصویر به مقیاس خاکستری
                        cropped_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                        # افزایش کنتراست با اعمال CLAHE
                        clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(1, 1))
                        cropped_image = clahe.apply(cropped_image)
                        patch = os.path.join(os.getcwd(), 'app', 'service', 'ml', 'a_id'+_id)
                        cv2.imwrite(patch, cropped_image)
                        plateNumber = self.model_Ocr.predict(patch)
                        if 'text' in plateNumber[0].keys():
                            plateNumber = plateNumber[0]['text']
                            if len(plateNumber) == 8:
                                try:
                                    idplate = int(plateNumber[:2])
                                    alpha = plateNumber[2:3]
                                    serial =int(plateNumber[3:6])
                                    city = int(plateNumber[6:])
                                    status = self.rule_model.get_statuse_by_plate(idplate, alpha, serial, city)
                                    try:
                                        self.rule_handle_model.CheckAllow(status)
                                    except:
                                        pass
                                    plates.append({'score':float(score), 'box':[x1, y1, x2, y2], 'number':{'idplate':idplate,'alpha':alpha,'serial':serial,'city':city}, 'status':status})
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"Score: {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                                except:
                                    pass

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')
            self.record_model.set_record(_id, ip, port, type, True, None, frame_bytes, plates, status)
        except:
            self.record_model.set_record(_id, ip, port, type, False, None, None, [], None)
            pass


    def record(self,_id):
        connection = self.connection_models.get_connection_by_id(_id)
        if connection['type'] == 'ip':
            username = connection['username']
            password = connection['password']
            ip = connection['ip']
            port = connection['port']
            rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/cam/realmonitor?channel=1&subtype=1"
            cap = cv2.VideoCapture(rtsp_url)
        else:
            cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            self.record_model.set_record(_id, ip, port, connection['type'], False, 'اتصال بر قرار نیست', None, [])
        else:
            while True:
                self.count += 1
                ret, frame = cap.read()
                if self.count == 10 and connection['type'] == 'ip':
                    self.prossece_plate(frame, _id, ip, port, connection['type'])
                    self.count = 0
                elif connection['type'] != 'ip':
                    time.sleep(0.1)
                    self.prossece_plate(frame, _id, None, None, connection['type'])
