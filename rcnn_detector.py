# rcnn_detector.py

import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision import transforms as T

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
    'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
    'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
    'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
    'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
    'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

desired_classes = {
    'car': 'car',
    'motorcycle': 'motorcycle',
    'truck': 'truck',
    'person': 'pedestrian'
}

class RCNNDetector:
    def __init__(self, threshold=0.5):
        self.model = fasterrcnn_resnet50_fpn(pretrained=True)
        self.model.eval()
        self.threshold = threshold
        self.transform = T.Compose([T.ToTensor()])

    def detect(self, frame):
        img_tensor = self.transform(frame)
        with torch.no_grad():
            preds = self.model([img_tensor])[0]

        detections = []
        for label, box, score in zip(preds['labels'], preds['boxes'], preds['scores']):
            label_name = COCO_INSTANCE_CATEGORY_NAMES[label.item()]
            if score.item() >= self.threshold:
                mapped_label = desired_classes.get(label_name, 'rest')
                detections.append({
                    'label': mapped_label,
                    'box': box.int().tolist(),
                    'score': score.item()
                })
        return detections
