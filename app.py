import os
import json
import re  # Used for safely parsing the AI's JSON response
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from ultralytics import YOLO

# --- CONFIGURATION ---

# [CRITICAL SECURITY] Load your API key from an environment variable.

from google import genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = None
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set this variable before running the app.")
    # In a real app, you might want to exit
else:
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        print("Gemini API configured successfully.")
    except Exception as e:
        print(f"Error configuring API key: {e}")

# [MODEL LOADING] Load your trained YOLO model
yolo_model = None
try:
    # Ensure 'best (6).pt' is in the same directory as app.py
    yolo_model = YOLO('best (6).pt')
    print("YOLO model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    print("Please make sure the model file is in the correct directory.")

# [FLASK SETUP]
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Create the 'uploads' folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- AI & DETECTION FUNCTIONS ---

def get_sorted_detections(image_path):
    """
    Runs the YOLO model on an image and returns a list of detections,
    sorted from top-to-bottom, then left-to-right.
    """
    if yolo_model is None:
        print("YOLO model is not loaded; skipping detection.")
        return []

    print(f"Running detection on {image_path}...")
    try:
        results = yolo_model(image_path)
    except Exception as e:
        print(f"Error during YOLO model prediction: {e}")
        return []

    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": yolo_model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 2),
                # [x_center, y_center, width, height]
                "box": [int(coord) for coord in box.xywh[0]]
            })

    # Sort detections: primarily by 'y' coordinate, secondarily by 'x'
    sorted_detections = sorted(detections, key=lambda d: (d['box'][1], d['box'][0]))

    print(f"Found and sorted {len(sorted_detections)} elements.")
    return sorted_detections

def generate_code_from_detections(detections):
    """
    Uses the Gemini model to generate a full HTML file, CSS, and an
    editable elements list based on the sorted YOLO detections.
    """
    if not detections:
        # Return a valid structure even if no detections
        return {"html": "<h2>No UI elements were detected.</h2>", "css": "", "editable_elements": []}

    if client is None:
        error_html = "<h2>Sorry, the AI client is not configured.</h2><p>Missing or invalid GOOGLE_API_KEY.</p>"
        return {"html": error_html, "css": "", "editable_elements": []}

    print("Sending detection data to Gemini for code generation...")

    detections_json = json.dumps(detections, indent=2)

    # This prompt is the most important part of the project.
    # It tells the AI *exactly* how to format its response.
    prompt = f"""
    You are an expert front-end web developer specializing in Bootstrap 5.
    Your task is to convert a JSON object of detected UI elements into a complete, standalone, responsive HTML file.

    HERE IS THE JSON DATA OF DETECTED ELEMENTS (sorted top-to-bottom):
    {detections_json}

    YOUR INSTRUCTIONS:
    1.  **Layout:** Use the bounding box data [x_center, y_center, width, height] to create a responsive Bootstrap 5 grid (`<div class="container">`, `<div class="row">`, `<div class="col-md-*">`). Elements with similar 'y_center' values should be in the same row.
    2.  **Full HTML Document:** You MUST generate a complete, valid HTML5 document. This includes `<!DOCTYPE html>`, `<html>`, `<head>`, `<title>Generated Page</title>`, the Bootstrap 5 CSS `<link>`, and the full `<body>`.
    3.  **Editable Elements (CRITICAL):** For EVERY UI element you generate (button, p, h1, img), you MUST add a unique `data-editable-id` attribute. Example: `data-editable-id="element-1"`, `data-editable-id="element-2"`.
    4.  **Placeholders:** Use good, clear placeholders.
        * For text/headings: "[Your Heading Here]" or "[Sample paragraph...]"
        * For images: Use `https://placehold.co/600x400` and YOU MUST add the class `img-fluid` to make them responsive.
    5.  **Output Format (STRICT):** Your entire response MUST be a single, minified JSON object. It must have THREE keys: "html", "css", and "editable_elements".
        * `"html"`: A string containing the complete standalone HTML document.
        * `"css"`: A string of any *additional* custom CSS. (Return an empty string "" if none is needed, do not return null).
        * `"editable_elements"`: A JSON array of objects. Each object must have "id" (matching the `data-editable-id`), "type" (e.g., "heading", "button", "image", "text"), and "default_content" (the placeholder text you used).

    EXAMPLE `editable_elements` FORMAT:
    [
      {{"id": "element-1", "type": "heading", "default_content": "[Your Heading Here]"}},
      {{"id": "element-2", "type": "image", "default_content": "https://placehold.co/600x400"}},
      {{"id": "element-3", "type": "button", "default_content": "Click Me"}}
    ]

    Now, generate the code based on the JSON data provided.
    """

    response = None
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        response_text = response.text

        # [ROBUST PARSING] Use regex to find the JSON block,
        # as the AI might add ```json ... ``` markers.
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)

        if not json_match:
            print("Error: No valid JSON object found in Gemini response.")
            print(f"Raw response: {response_text}")
            raise ValueError("No valid JSON object found in the model's response.")

        clean_response_text = json_match.group(0)
        code_dict = json.loads(clean_response_text)

        print("Gemini response parsed successfully.")
        return code_dict

    except Exception as e:
        print(f"An error occurred during Gemini code generation: {e}")
        # Return an error structure that the frontend can still render
        error_html = f"<h2>Sorry, an error occurred during code generation.</h2><p>{e}</p>"
        if response is not None:
            error_html += f"<pre>Raw Response:\n{response.text}</pre>"
        return {"html": error_html, "css": "", "editable_elements": []}

# --- WEB ROUTES ---

@app.route('/')
def index():
    """Serves the main upload page (index.html)."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles the file upload and the entire AI pipeline."""
    if 'sketch_file' not in request.files:
        print("No file part in request.")
        return redirect(request.url)

    file = request.files['sketch_file']

    if file.filename == '':
        print("No file selected.")
        return redirect(request.url)

    if file:
        # Make the filename safe
        filename = secure_filename(file.filename)
        # Save the file to our 'uploads' folder
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
        print(f"File saved to {image_path}")

        # --- This is the main pipeline ---
        # 1. Run YOLO detection on the saved image
        sorted_detections = get_sorted_detections(image_path)
        # 2. Send detection results to Gemini to generate code
        code_data = generate_code_from_detections(sorted_detections)
        # ---------------------------------

        # 3. Render the result.html page, passing in all the
        #    generated data (html, css, and the elements list).
        return render_template(
            'result.html',
            generated_html=code_data.get('html', 'Error: No HTML returned.'),
            generated_css=code_data.get('css', '/* No CSS returned */'),
            editable_elements=code_data.get('editable_elements', [])
        )

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Runs the Flask app
    # debug=True means the server will auto-reload when you save the file
    app.run(debug=True)