from ultralytics import YOLO
from PIL import Image

def get_detections(image_path):
    """
    Takes an image path, runs detection, and returns a list of results.
    """
    model = YOLO('best (6).pt') # Your trained model
    img = Image.open(image_path)
    results = model.predict(img)
    
    detections = []
    
    for r in results:
        boxes = r.boxes
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            # Get the y-coordinate to sort by
            y1 = box.xyxy[0][1].item() 
            
            detections.append({
                'class': class_name,
                'y': y1,
                'box': box.xyxy[0].tolist() # Full coordinates
            })
            
    # Sort detections from top to bottom
    detections.sort(key=lambda d: d['y'])
    
    return detections