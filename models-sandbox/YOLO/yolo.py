from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

# Load a model
model = YOLO("yolov8n-seg.yaml")  # build a new model from YAML
model = YOLO("yolov8n-seg.pt")  # load a pretrained model (recommended for training)


# Train the model
results = model.train(data="coco8-seg.yaml", epochs=100, imgsz=640)
