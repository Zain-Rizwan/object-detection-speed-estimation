# rcnn_gui.py

import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
from rcnn_detector import RCNNDetector
from tracker import ObjectTracker
from speed_estimator import SpeedEstimator
from counter import VehicleCounter

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Counter & Speed Estimator (RCNN)")
        self.canvas = tk.Canvas(root, width=1280, height=720)
        self.canvas.pack()

        self.video_path = None
        self.roi = None
        self.detector = RCNNDetector()
        self.tracker = ObjectTracker()
        self.speed_estimator = SpeedEstimator()
        self.counter = VehicleCounter()
        self.start_x = None
        self.start_y = None
        self.rect_id = None


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
            self.display_frame(frame)
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_move_press)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_move_press(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = event.x, event.y
        self.roi = (min(self.start_x, end_x), min(self.start_y, end_y),
                max(self.start_x, end_x), max(self.start_y, end_y))
        print(f"ROI selected: {self.roi}")


    def select_roi(self, event):
        x, y = event.x, event.y
        self.roi = (x, y, x+100, y+100)
        print(f"ROI selected: {self.roi}")

    def display_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

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

            # for obj in tracked:
            #     obj_id, label, box = obj['id'], obj['label'], obj['box']
            for obj in tracked:
                obj_id, label, box = obj['id'], obj['label'], obj['box']
                x1, y1, x2, y2 = box
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # center of the box

                # Only process if center is within ROI
                if self.roi:
                    rx1, ry1, rx2, ry2 = self.roi
                    if not (rx1 <= cx <= rx2 and ry1 <= cy <= ry2):
                        continue  # Skip objects outside ROI

                speed = self.speed_estimator.estimate(obj_id, box)
                self.counter.count(obj_id, label)

                color = (0, 0, 255) if speed > 30 else (0, 255, 0)
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} ID:{obj_id} {speed:.1f} km/h", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            frame = self.counter.draw_counts(frame)
            self.display_frame(frame)
            self.root.update_idletasks()
            self.root.update()

        print("Final Counts:", self.counter.get_counts())
