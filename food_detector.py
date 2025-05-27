from imageai.detection import ObjectDetection
import os

detector = ObjectDetection()
model_path = os.path.join("models", "yolo.h5")
detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

def detect_food(image_path):
    detections = detector.detectObjectsFromImage(
        input_image=image_path,
        output_image_path=os.path.join("static", "output.jpg"),
        minimum_percentage_probability=40
    )
    food_item = [d["name"] for d in detections]
    return list(set(food_item)) # remove duplicates