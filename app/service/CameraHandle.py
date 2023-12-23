from app.models.Record import Record
from app.models.Connection import Connection
from hezar.models import Model
from app.models.Rules import Rulse

import cv2
import yolov5
import time
import base64
import torch
import os
from transformers import YolosImageProcessor, YolosForObjectDetection

class CameraHandle():
    def __init__(self):
        self.record_model = Record()
        self.connection_models = Connection()
        self.cap = None
        model_path = os.path.join(os.getcwd(), 'app', 'service', 'ml', 'yolov5n-license-plate', 'best.pt')
        self.model = yolov5.load(model_path)
        try:
            self.device = "cuda"
            self.model = self.model.to(self.device)
        except:
            self.device = "cpu"
            self.model = self.model.to(self.device)
        print(torch.cuda.is_available())
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
                        path = os.path.join(os.getcwd(), 'app', 'service','temp', f'a_{_id}.jpg')
                        cv2.imwrite(path, cropped_image)
                        plateNumber = self.model_Ocr.predict(path)
                        if 'text' in plateNumber[0].keys():
                            plateNumber = plateNumber[0]['text']
                            if len(plateNumber) == 8:
                                try:
                                    idplate = int(plateNumber[:2])
                                    alpha = plateNumber[2:3]
                                    serial =int(plateNumber[3:6])
                                    city = int(plateNumber[6:])
                                    plates.append({'score':float(score), 'box':[x1, y1, x2, y2], 'number':{'idplate':idplate,'alpha':alpha,'serial':serial,'city':city}})
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                    cv2.putText(frame, f"Score: {score:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                                except:
                                    pass

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')
            self.record_model.set_record(id_camera=_id, ip=ip, port=port, type=type, connect=True, error=None, image=frame_bytes, plate=plates, status=status)
        except:
            #_, buffer = cv2.imencode('.jpg', frame)
            #frame_bytes = buffer.tobytes()
            #frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')
            #self.record_model.set_record(_id, ip, port, type, False, None, frame_bytes, [], None)
            pass
    
    def Detect_Object(self, frame, _id, ip, port):
        inputs = self.image_processor(images=frame, return_tensors="pt")
        outputs = self.model_Object(**inputs)
        logits = outputs.logits
        bboxes = outputs.pred_boxes
        target_sizes = torch.tensor([frame.shape[1::-1]])
        results = self.image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
        res = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            # Draw bounding box on the image
            start_point = (int(box[0]), int(box[1]))
            end_point = (int(box[2]), int(box[3]))
            color = (0, 255, 0)  # Green color
            thickness = 2
            frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
            lbl = self.model_Object.config.id2label[label.item()]
            scr = round(score.item(), 3)
            dic = {'label':lbl,'score':scr}
            res.append(dic)
            label_text = f"{lbl}: {scr}"
            org = (int(box[0]), int(box[1]) - 10)  # Above the box
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_color = (100, 255, 255)  # White color
            line_type = 1
            frame = cv2.putText(frame, label_text, org, font, font_scale, font_color, line_type)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')
        self.record_model.set_record(id_camera=_id, ip=ip, port=port, rule_type='tttt', connect=True, error=None, image=frame_bytes, plate=[], status=1, obj=res)

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
            self.record_model.set_record(id_camera=_id, ip=ip, port=port, type=connection['type'], connect=False, error='اتصال بر قرار نیست', image=None, plate=[], status=None)
        else:
            while True:
                self.count += 1
                ret, frame = cap.read()
                if self.count == 10 and connection['type'] == 'ip':
                    self.prossece_plate(frame, _id, ip, port, connection['type'])
                    self.count = 0
                elif connection['type'] != 'ip' :
                    time.sleep(0.1)
                    self.prossece_plate(frame, _id, None, None, connection['type'])

