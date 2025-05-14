import cv2

def draw_info(frame, detections, speeds, vehicle_counts):
    for det in detections:
        label = det["label"]
        x1, y1, x2, y2 = det["box"]
        center = det["center"]
        obj_id = center  # Using center as ID (simplified)

        speed = speeds.get(obj_id, 0)
        color = (0, 0, 255) if speed > 30 else (0, 255, 0)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {int(speed)} km/h", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    y = 20
    for k, v in vehicle_counts.items():
        cv2.putText(frame, f"{k}: {v}", (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y += 25

    return frame
