from ultralytics import YOLO

import os

# טען את המודל (YOLOv8n - הקל והמהיר)
model = YOLO("yolov8n.pt")  # ודא שהקובץ נמצא בתיקייה הראשית או תן נתיב מלא

def detect_food(image_path: str) -> list:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"תמונה לא נמצאה: {image_path}")
    
    results = model(image_path)
    detections = results[0].boxes.data.cpu().numpy()

    names = results[0].names
    labels = [names[int(cls)] for cls in results[0].boxes.cls]

    return labels
