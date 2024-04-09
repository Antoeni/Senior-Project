# new code to resize the video
# this is for UI

import tkinter as tk
from tkinter import ttk
import sv_ttk

from ultralytics import YOLO
from ultralytics.solutions import heatmap
import cv2
import json


root = tk.Tk()

sv_ttk.use_dark_theme()


class Heatmap:
    def __init__(self, master):
        self.master = master
        self.master.title("Heatmap")
        self.canvas = tk.Canvas(master, width=800, height=800)
        self.canvas.pack()

        self.model = YOLO("best_2-23.pt")
        self.f = open('dataOutput2', 'a')
        self.names = self.model.names
        #for the video capture
        self.cap = cv2.VideoCapture('vidp.mp4')
        assert self.cap.isOpened(), "Error reading video file"
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.target_width = 1280
        self.target_height = 720

        self.video_writer = cv2.VideoWriter("heatmap_output.avi",
                                       cv2.VideoWriter_fourcc(*'mp4v'),
                                       self.fps,
                                       (self.target_width, self.target_height))
        self.heatmap_obj = heatmap.Heatmap()
        self.heatmap_obj.set_args(colormap=cv2.COLORMAP_PLASMA,
                             imw=self.target_width,
                             imh=self.target_height,
                             view_img=True,
                             shape="circle")
        self.heatmap_creation()

    def heatmap_creation(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            frame = cv2.resize(frame, (self.target_width, self.target_height))

            tracks = self.model.track(frame, persist=True, show=False, verbose=True, classes=0)
            name = tracks[0].self.names
            personDetection = []
            for k, v in name.items():
                personDetection.append(tracks[0].boxes.cls.tolist().count(k))


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # Resize frame to target dimensions
    frame = cv2.resize(frame, (target_width, target_height))

    # Perform object tracking
    tracks = model.track(frame, persist=True, show=False, verbose=True, classes=0)
    name = tracks[0].names
    personDetection = []
    for k, v in name.items():
        personDetection.append(tracks[0].boxes.cls.tolist().count(k))
    detected = dict(zip(names.values(), personDetection))
    with open('dataOutput.txt', 'w') as convert_file:
        convert_file.write(json.dumps(detected))
    print(detected)
    frame = heatmap_obj.generate_heatmap(frame, tracks)
    # Write frame to output video
    video_writer.write(frame)

    if cv2.waitKey(1) == ord("q"):
        break

f.close()
cap.release()
video_writer.release()
cv2.destroyAllWindows()