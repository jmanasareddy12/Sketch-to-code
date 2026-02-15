# Import the functions from your new files
from detector import get_detections
from generator import generate_html

# 1. Define your sketch image
image_to_process = 'YOUR_SKETCH_IMAGE.jpg' 

# 2. STAGE 1: Get the detections
print(f"Running detection on {image_to_process}...")
all_detections = get_detections(image_to_process)
print(f"Found {len(all_detections)} components.")
print(all_detections) # This lets you debug Stage 1

# 3. STAGE 2: Generate the HTML
print("Generating HTML...")
final_html = generate_html(all_detections)

# 4. Save the final result
with open("output.html", "w") as f:
    f.write(final_html)
    
print("All done! 'output.html' has been created.")