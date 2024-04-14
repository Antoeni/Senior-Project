# new code to resize the video
from ultralytics import YOLO
from ultralytics.solutions import heatmap
import cv2
import json

model = YOLO("best_2-23.pt")
cap = cv2.VideoCapture('vidp.mp4')
f = open('dataOutput2', 'a')
names = model.names
assert cap.isOpened(), "Error reading video file"
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define target width and height
target_width = 1280
target_height = 720

# Video writer
video_writer = cv2.VideoWriter("heatmap_output.avi",
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps,
                               (target_width, target_height))

# Init heatmap
heatmap_obj = heatmap.Heatmap()
heatmap_obj.set_args(colormap=cv2.COLORMAP_WINTER,
                     imw=target_width,
                     imh=target_height,
                     view_img=True,
                     shape="circle")

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