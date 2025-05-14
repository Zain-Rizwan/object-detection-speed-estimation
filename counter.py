import cv2

class VehicleCounter:
    def __init__(self):
        self.counted_ids = set()
        self.counts = {
            'car': 0,
            'truck': 0,
            'motorcycle': 0,
            'person': 0,
            'rest': 0
        }
        self.valid_labels = {'car', 'truck', 'motorcycle', 'person'}

    def count(self, obj_id, label):
        if obj_id not in self.counted_ids:
            if label in self.valid_labels:
                self.counts[label] += 1
            else:
                self.counts['rest'] += 1
            self.counted_ids.add(obj_id)

    def draw_counts(self, frame):
        y = 30
        for label, count in self.counts.items():
            cv2.putText(frame, f"{label}: {count}", (10, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            y += 40
        return frame

    def get_counts(self):
        return self.counts
