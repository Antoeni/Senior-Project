# new code to resize the video
from ultralytics import YOLO
from ultralytics.solutions import heatmap
import threading
import cv2
import json

model1 = YOLO("best-4_5.pt")
model2 = YOLO('best-4_5.pt')
video1 = 0
video2 = 'Shibuya crossing real-time.mp4'


def threadRun(vidName, model, outputFile):
    cap = cv2.VideoCapture(vidName)
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
    heatmap_obj.set_args(colormap=cv2.COLORMAP_PLASMA,
                         imw=target_width,
                         imh=target_height,
                         view_img=False,
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
        with open(outputFile, 'w') as convert_file:
            convert_file.write(json.dumps(detected))
        print(vidName)
        print(detected)
        frame = heatmap_obj.generate_heatmap(frame, tracks)
        cv2.imshow(str(vidName), frame)
        # Write frame to output video
        video_writer.write(frame)

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()


tracker_thread1 = threading.Thread(target=threadRun, args=(video1, model1, 'dataOutput.txt'), daemon=True)
tracker_thread2 = threading.Thread(target=threadRun, args=(video2, model2, 'dataOutput2'), daemon=True)
tracker_thread1.start()
tracker_thread2.start()

tracker_thread1.join()
tracker_thread2.join()
