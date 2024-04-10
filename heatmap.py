import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import json
from ultralytics import YOLO
from ultralytics.solutions import heatmap


class Heatmap(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self)
        self.master = master
        self.master.title("Heatmap UI")
        self.video_source = 'Shibuya crossing real-time.mp4'
        self.cap = cv2.VideoCapture(self.video_source)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fpsOut = self.fps * 7
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.target_width = 640
        self.target_height = 480

        self.canvas = tk.Canvas(master, width=self.target_width, height=self.target_height)
        self.canvas.pack()

        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        self.var_5 = tk.DoubleVar(value=75.0)

        self.model = YOLO("best-4_5.pt")
        self.names = self.model.names
        self.detected_text = tk.StringVar()

        self.heatmap_obj = heatmap.Heatmap()
        self.heatmap_obj.set_args(colormap=cv2.COLORMAP_PLASMA,
                                  imw=self.target_width,
                                  imh=self.target_height,
                                  view_img=True,
                                  shape="circle")

        self.Heatmap_creation()
        self.setup_widgets()

    def setup_widgets(self):
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=1, pady=(25, 5), sticky="nsew", rowspan=3)
        # Notebook, pane #2
        self.pane_2 = ttk.Frame(self.paned, padding=5)
        self.paned.add(self.pane_2, weight=3)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_2)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Person Detected")

        # Label
        self.label = ttk.Label(
            self.tab_1,
            textvariable=self.detected_text,
            justify="center",
            font=("-size", 15, "-weight", "bold"),
        )
        self.label.grid(row=1, column=0, pady=10, columnspan=2)

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
    def Heatmap_creation(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (self.target_width, self.target_height))

                tracks = self.model.track(frame, persist=True, show=False, verbose=True, classes=0)
                name = tracks[0].names
                personDetection = []
                for k, v in name.items():
                    personDetection.append(tracks[0].boxes.cls.tolist().count(k))
                detected = dict(zip(self.names.values(), personDetection))
                with open('dataOutput.txt', 'w') as convert_file:
                    convert_file.write(json.dumps(detected))
                print(detected)

                # Read detected values from the file
                with open('dataOutput.txt', 'r') as file:
                    detected_from_file = json.load(file)

                # Update the label text with the values from the file
                self.detected_text.set(json.dumps(detected_from_file))
                frame = self.heatmap_obj.generate_heatmap(frame, tracks)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.master.after(int(1000 / self.fpsOut), self.Heatmap_creation)
            else:
                self.cap.release()
                self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("")

    # Simply set the theme
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")

    app = Heatmap(root)
    app.pack(fill="both", expand=True)

    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

    root.mainloop()