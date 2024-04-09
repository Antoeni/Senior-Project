from ultralytics import YOLO

model = YOLO('yolov8n.yaml')  # build a new model from YAML
model = YOLO('best_2-23.pt')  # load a pretrained model (recommended for training)
model = YOLO('yolov8n.yaml').load('best_2-23.pt')  # build from YAML and transfer weights

# Train the model
results = model.train(data='config.yaml', epochs=100, imgsz=640)