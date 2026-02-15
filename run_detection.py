from ultralytics import YOLO
from PIL import Image

# 1. Load your local model
model = YOLO('best.pt')  # <-- It finds the file in the same folder

# 2. Load your local sketch image
# ⚠️ Make sure to update this path!
img_path = 'test_image1.jpg'
img = Image.open(img_path)

# 3. Run the prediction
results = model.predict(img)

# 4. This is the "shopping list" for Stage 2
print("--- DETECTIONS FOUND ---")
detections = [] # A list to store our findings

for r in results:
    boxes = r.boxes
    for box in boxes:
        # Get coordinates
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        # Get class name
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        
        # Store the detection
        detection_data = {
            'class': class_name,
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2
        }
        detections.append(detection_data)
        
        print(f"Found: {class_name}, at Coords: [{x1}, {y1}, {x2}, {y2}]")

# Now 'detections' is a Python list containing all your data
# You can pass this list to your Stage 2 layout generator