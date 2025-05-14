import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from yolo_detector import YOLODetector
from tracker import ObjectTracker
from speed_estimator import SpeedEstimator
from counter import VehicleCounter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Counter & Speed Estimator")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.video_path = None
        self.roi = None
        self.roi_start = None
        self.roi_end = None
        self.rect_id = None

        self.detector = YOLODetector()
        self.tracker = ObjectTracker()
        self.speed_estimator = SpeedEstimator()
        self.counter = VehicleCounter()

        self.setup_gui()

    def setup_gui(self):
        tk.Button(self.root, text="Select Video", command=self.load_video).pack()
        tk.Button(self.root, text="Start", command=self.start_processing).pack()

    def load_video(self):
        self.video_path = filedialog.askopenfilename()
        self.cap = cv2.VideoCapture(self.video_path)
        ret, frame = self.cap.read()
        if ret:
            self.first_frame = frame.copy()
            height, width = frame.shape[:2]
            self.canvas.config(width=width, height=height)
            self.display_frame(frame)
            self.canvas.bind("<ButtonPress-1>", self.start_roi)
            self.canvas.bind("<B1-Motion>", self.draw_roi)
            self.canvas.bind("<ButtonRelease-1>", self.end_roi)

    def start_roi(self, event):
        self.roi_start = (event.x, event.y)
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = None

    def draw_roi(self, event):
        if self.roi_start:
            if self.rect_id:
                self.canvas.delete(self.rect_id)
            self.roi_end = (event.x, event.y)
            self.rect_id = self.canvas.create_rectangle(
                self.roi_start[0], self.roi_start[1],
                self.roi_end[0], self.roi_end[1],
                outline='red'
            )

    def end_roi(self, event):
        self.roi_end = (event.x, event.y)
        x1, y1 = self.roi_start
        x2, y2 = self.roi_end
        self.roi = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        print(f"ROI selected: {self.roi}")

    def display_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img  # Keep a reference to prevent garbage collection
    def start_processing(self):
        if not self.video_path:
            print("No video selected.")
            return

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            detections = self.detector.detect(frame)
            tracked = self.tracker.update(detections)

            for obj in tracked:
                obj_id, label, box = obj['id'], obj['label'], obj['box']
                x1, y1, x2, y2 = box
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Center of the bounding box

                # Only process if center is inside ROI
                if self.roi:
                    rx1, ry1, rx2, ry2 = self.roi
                    if not (rx1 <= cx <= rx2 and ry1 <= cy <= ry2):
                        continue  # Skip this object if not in ROI

                speed = self.speed_estimator.estimate(obj_id, box)
                self.counter.count(obj_id, label)

                color = (0, 0, 255) if speed > 30 else (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} ID:{obj_id} {speed:.1f} km/h", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            frame = self.counter.draw_counts(frame)

            # Optionally draw ROI for reference
            if self.roi:
                rx1, ry1, rx2, ry2 = self.roi
                cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)

            self.display_frame(frame)
            self.root.update_idletasks()
            self.root.update()

        print("Final Counts:", self.counter.get_counts())

    # def start_processing(self):
    #     if not self.video_path:
    #         print("No video selected.")
    #         return

    #     while True:
    #         ret, frame = self.cap.read()
    #         if not ret:
    #             break

    #         detections = self.detector.detect(frame)
    #         tracked = self.tracker.update(detections)

    #         for obj in tracked:
    #             obj_id, label, box = obj['id'], obj['label'], obj['box']
    #             speed = self.speed_estimator.estimate(obj_id, box)
    #             self.counter.count(obj_id, label)

    #             color = (0, 0, 255) if speed > 30 else (0, 255, 0)
    #             x1, y1, x2, y2 = box
    #             cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    #             cv2.putText(frame, f"{label} ID:{obj_id} {speed:.1f} km/h", (x1, y1 - 10),
    #                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    #         frame = self.counter.draw_counts(frame)

    #         # Optionally draw the selected ROI
    #         if self.roi:
    #             rx1, ry1, rx2, ry2 = self.roi
    #             cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)

    #         self.display_frame(frame)
    #         self.root.update_idletasks()
    #         self.root.update()

    #     print("Final Counts:", self.counter.get_counts())
