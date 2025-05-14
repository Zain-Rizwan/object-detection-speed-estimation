class ObjectTracker:
    def __init__(self):
        self.next_id = 0
        self.tracks = {}

    def update(self, detections):
        updated = []
        for det in detections:
            box = det['box']
            label = det['label']
            matched_id = self.match_object(box)

            if matched_id is None:
                matched_id = self.next_id
                self.next_id += 1

            self.tracks[matched_id] = box
            updated.append({'id': matched_id, 'label': label, 'box': box})

        return updated

    def match_object(self, new_box):
        # Dummy IoU matching for simplicity
        for obj_id, old_box in self.tracks.items():
            if self.iou(old_box, new_box) > 0.4:
                return obj_id
        return None

    def iou(self, box1, box2):
        xA = max(box1[0], box2[0])
        yA = max(box1[1], box2[1])
        xB = min(box1[2], box2[2])
        yB = min(box1[3], box2[3])
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
        box1Area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
        box2Area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)
        return interArea / float(box1Area + box2Area - interArea)
