# Sketch to Code (S2C)

A simple AI-powered **Sketch → HTML Code Generator** built using Python and Flask.
This project converts hand-drawn UI sketches into structured HTML code using computer vision and generative AI.

---

## 🚀 Features

* Upload hand-drawn UI sketches
* Object detection for UI components
* AI-generated HTML layout
* Live preview of generated code
* Flask-based web interface
* Easy-to-extend architecture

---

## 🛠️ Tech Stack

* Python
* Flask
* OpenCV
* PyTorch (model inference)
* Google Generative AI (Gemini)
* HTML / CSS

---

## 📂 Project Structure

```
s2c/
│
├── app.py                # Main Flask application
├── detector.py           # UI element detection logic
├── generator.py          # Code generation logic
├── run_detection.py      # Detection runner
├── templates/            # HTML templates
├── uploads/              # Uploaded images
├── requirements.txt      # Project dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/jmanasareddy12/Sketch-to-code.git
cd Sketch-to-code
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/Mac**

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 📸 How It Works

1. Upload a sketch image
2. Detection model identifies UI components
3. AI generates HTML layout
4. Preview generated result live in browser

---

## 🧠 Future Improvements

* Better UI component detection
* Drag-and-edit generated layouts
* Export to React / Tailwind
* Improved styling generation
* Deployment support

---

## 👩‍💻 Author

**J Manasa Reddy**

---

## ⭐ Acknowledgements

* Inspired by Microsoft Sketch2Code concept
* Powered by modern AI and computer vision tools

---
