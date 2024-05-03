# Human-Detection-with-Heat-map
An application that detects humans from a camera and presents the population density as a heap map.
Utilizes YOLO, OpenCV, and other Machine Learning Libraries for detecting human objects accurately. 

## Installation
Libraries required:

Import library needed for this project.
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import json
from ultralytics import YOLO
from ultralytics.solutions import heatmap

Include pip install instructions

pip install sv-ttk #installs the UI
pip install ultralytics #installs the dependencies


## Usage
How do users use your program/code
```
$ python3 heatmap.py #FOR MAC
$ python .\heatmap.py #FOR WINDOWS

```
### Testing

The application will take in a camera source/video source, which it will display directly onto the UI what the source is from. 
Users will then be able to see what the heatmap is creating through the video source.

### Utilizing a webcam / camera

The webcam is going to capture the data in order for the AI to predict successfully what is in front of it. 
Then it will create a heatmap based on what is being detected from the AI.

## Features

What are some of the features of the projects. What can people do and how to use it. 
1. Camera
>  > Detector people in static or motion.
>  > Set more than one camera. Different view points. Will the camera recongize the same human and only count 1.
2. Heat Map
>  > Creates a heatmap based on the AI detection
3. AI
>  > Utilizes the AI to predict what it is seeing on the video source.

## Sample Image
![image](https://github.com/kerrycliu/Human-Detection-with-Heat-map/assets/93110676/1d287e7f-d2a5-47c3-969f-f544c534b32e)

## Roadmap
1. Using CVAT, an open-source image and video annotation tool, to accurately detect humans only.
2. Use Yolov8 as the AI model to predict humans. 
3. Utilize AI in order to predict a human based on detections.
4. Gather human count from each camera frame.
5. Generate heatmap based on the data. 

## Contacts
Michelle Fang:

Kerry Liu:
PHONE: (510)3201972
EMAIL: chinan.liu@sjsu.edu

Anthony Nguyen: 
PHONE:(408)7057746

EMAIL:hoanganthony.nguyen@sjsu.edu

Klein Sicam:
