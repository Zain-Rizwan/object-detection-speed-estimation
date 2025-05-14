from ultralytics import YOLO

class YOLODetector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")  # You can switch to yolov8s.pt etc.

    def detect(self, frame):
        results = self.model.predict(frame, conf=0.4)[0]
        detections = []
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, cls = map(int, r[:6])
            label = self.model.names[int(cls)]
            if label in ['car', 'truck', 'motorcycle', 'person']:
                detections.append({'label': label, 'box': (x1, y1, x2, y2)})
        return detections
