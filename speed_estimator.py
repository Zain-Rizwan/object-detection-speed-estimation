import time
import numpy as np

class SpeedEstimator:
    def __init__(self):
        self.history = {}

    def estimate(self, obj_id, box):
        now = time.time()
        center = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)
        if obj_id in self.history:
            prev_center, prev_time = self.history[obj_id]
            distance = np.linalg.norm(np.array(center) - np.array(prev_center))
            time_elapsed = now - prev_time
            speed_px_per_sec = distance / time_elapsed if time_elapsed > 0 else 0
            speed_kmph = speed_px_per_sec * 0.068  # ~0.068 from 8x20 pixel = 1 sqft approx
        else:
            speed_kmph = 0

        self.history[obj_id] = (center, now)
        return speed_kmph
