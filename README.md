# ♻️ Go green — Smart Waste Classifier

> **AI-Powered Waste Sorting & Recycling Assistant using Computer Vision**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Online-success?style=for-the-badge&logo=google-chrome)](http://15.134.218.61/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black?style=for-the-badge&logo=flask)](https://palletsprojects.com/p/flask/)
[![TensorFlow Lite](https://img.shields.io/badge/TensorFlow%20Lite-Inference-orange?style=for-the-badge&logo=tensorflow)](https://www.tensorflow.org/lite)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=for-the-badge&logo=bootstrap)](https://getbootstrap.com/)

---

## 🌐 Live Deployment

Try out the application live in your browser:
👉 **[http://15.134.218.61/](http://15.134.218.61/)**

---

## 📖 Overview

Improper waste disposal and lack of source segregation are major contributors to environmental pollution and low municipal recycling rates. **Go green** (Smart Waste Classifier) helps users instantly identify the type of waste they are holding and provides practical, category-specific disposal instructions (Do's & Don'ts).

Users can capture a photo with their mobile camera or upload an existing image. The application analyzes the photo using an optimized **MobileNetV2** deep learning model running on **TensorFlow Lite**, returning top predictions, confidence scores, and recycling advice in seconds.

---

## ✨ Key Features

### 👤 User Experience
* **Instant Photo Classification**: Drag-and-drop or select photos from your device, or use your phone's camera directly.
* **Client-Side Image Optimization**: Resizes and compresses images in the browser before upload to minimize data usage and latency on mobile networks.
* **Smart Confidence Thresholding**: Distinguishes confident predictions from uncertain ones to avoid misleading users when photos are blurry or poorly lit.
* **Actionable Recycling Advice**: Clear **Do's** and **Don'ts** tailored to each category, plus general eco-tips.
* **User Feedback Loop**: Users can confirm predictions (thumbs up) or suggest corrections (thumbs down + label picker) to help monitor real-world accuracy.
* **Dark / Light Mode**: Seamless dark mode support with automatic OS preference detection and manual toggle persistence.
* **Comprehensive Waste Guide & FAQ**: Built-in guide covering materials, preparation tips, and disposal guidelines.

### 🛡️ Admin & Analytics Portal
* **Role-Based Authentication**: Secure admin login with hashed credentials (`werkzeug.security`).
* **Visual Dashboard**: Powered by **Chart.js**, displaying:
  * Total classifications and average model confidence.
  * Category distribution (Doughnut chart) and counts (Bar chart).
  * 14-day daily classification trends (Line chart).
  * User-reported accuracy and top confusion/mistake pairs.
* **Prediction History Log**: Paginated records with thumbnail previews, status tags, confidence percentages, and timestamps.
* **Filter & Search**: Filter history by waste category and prediction status (`OK`, `Uncertain`, `Other`).
* **Data Management**: Delete single entries (removes record and uploaded image) or export the entire history to **CSV**.

---

## 🏷️ Supported Waste Categories

The model is trained to recognize 6 primary waste streams:

| Category | Emoji | Examples | Key Disposal Rule |
| :--- | :---: | :--- | :--- |
| **Cardboard** | 📦 | Boxes, cartons, packaging | Flatten boxes, keep dry, remove tape. |
| **Glass** | 🍾 | Bottles, food jars | Rinse clean, separate lids, wrap broken glass safely. |
| **Metal** | 🥫 | Beverage cans, tins, metal scrap | Rinse cans, crush to save space. |
| **Organic** | 🍎 | Food scraps, peels, fruit/vegetable waste | Wet waste bin or home compost; drain liquids. |
| **Paper** | 📄 | Newspapers, office sheets, magazines | Keep clean & dry; do not recycle grease-soaked paper. |
| **Plastic** | 🧴 | Bottles, containers, clean packaging | Empty and rinse; remove non-recyclable caps/labels. |

> *Note: Special and hazardous waste (e.g. batteries, electronics, medicines, chemicals) should never go into regular bins. Follow your local municipality's hazardous/e-waste collection guidelines.*

---

## 🛠️ Technology Stack

* **Backend**: Python 3, [Flask 3.1](https://flask.palletsprojects.com/), Gunicorn (WSGI)
* **Computer Vision & Inference**:
  * Base Model: [MobileNetV2](https://arxiv.org/abs/1801.04381) (pre-trained on ImageNet)
  * Framework: TensorFlow / Keras (Training)
  * Deployment Runtime: [Google LiteRT](https://ai.google.dev/edge/litert) (`ai-edge-litert`) / TensorFlow Lite
  * Image Processing: Pillow (PIL), NumPy
* **Database**: SQLite3 with thread-safe connection pooling
* **Frontend**: HTML5, CSS3, JavaScript (ES6+), [Bootstrap 5.3](https://getbootstrap.com/), [Bootstrap Icons](https://icons.getbootstrap.com/), [Chart.js 4.4](https://www.chartjs.org/)

---

## 📁 Project Structure

```text
smart-waste-classifier/
├── app.py                      # Flask routes and application entry point
├── config.py                   # App configuration & path constants
├── requirements.txt            # Production Python dependencies
├── reset_admin.py              # Utility to create or reset admin credentials
├── create_admin.py             # Script to initialize admin account
├── predict_test.py             # CLI testing script for predictions
├── check_dataset.py            # Dataset integrity verification script
├── balance_dataset.py          # Class rebalancing utility
├── split_dataset.py            # Train/validation/test split tool
├── train_model.py              # MobileNetV2 transfer learning training pipeline
├── convert_tflite.py           # Keras to TensorFlow Lite conversion script
│
├── model/
│   ├── class_names.json        # List of supported classification labels
│   └── waste_classifier.tflite # Optimized, quantized TFLite inference model (~8.6 MB)
│
├── utils/
│   ├── classifier.py           # TFLite inference engine with thread locking
│   ├── db.py                   # SQLite schema, queries, analytics, and history
│   └── recommendations.py      # Category rules, eco tips, and disposal guidance
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Shared layout, navbar, footer, theme script
│   ├── index.html              # Main photo upload & classification page
│   ├── result.html             # Classification results, breakdown & feedback form
│   ├── guide.html              # Comprehensive recycling guide
│   ├── about.html              # Project overview and limitations
│   ├── login.html              # Admin login page
│   ├── dashboard.html          # Admin analytics dashboard with charts
│   └── history.html            # Admin prediction history log with filters
│
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles, responsive tweaks & dark mode theme
│   ├── js/
│   │   ├── main.js             # Image resizing, upload validation, drag-and-drop
│   │   └── dashboard.js        # Chart.js rendering for analytics
│   └── uploads/                # Directory for user-uploaded images
│
└── outputs/                    # Training evaluation artifacts
    ├── classification_report.txt # Test set precision, recall, f1-score (86.5% accuracy)
    ├── confusion_matrix.png      # Confusion matrix visualization
    └── training_curves.png       # Loss and accuracy curves across training phases
```

---

## 🚀 Getting Started (Local Development)

### 1. Prerequisites
* Python 3.10, 3.11, or 3.12
* `pip` and `venv`

### 2. Clone Repository
```bash
git clone https://github.com/mdAsadAlamgithub/smart-waste-classifier.git
cd smart-waste-classifier
```

### 3. Create and Activate Virtual Environment
```bash
python3 -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Create an Admin Account
Initialize the SQLite database and create your administrative login:
```bash
python reset_admin.py
```
Follow the prompt to enter your desired username and password (minimum 8 characters).

### 6. Run the Application
```bash
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000/`**

---

## 🧠 Model Training & Performance

The classifier is built on **MobileNetV2** through transfer learning, optimized for both inference speed and classification accuracy:

1. **Preprocessing & Augmentation**:
   * Input resolution: $224 \times 224 \times 3$.
   * Augmentation layers: Random Horizontal Flip, Rotation ($\pm 10\%$), Zoom ($\pm 15\%$), Brightness ($\pm 20\%$), and Contrast ($\pm 20\%$).
   * Built-in Rescaling layer (normalized to $[-1, 1]$).
2. **Two-Stage Training Process**:
   * **Phase A (Head Training)**: Frozen base model with a newly attached GlobalAveragePooling2D, Dropout (0.3), and Softmax dense layer trained with Adam optimizer (`lr=1e-3`).
   * **Phase B (Fine-Tuning)**: Unfreezing the top 30 layers with reduced learning rate (`lr=1e-5`) and early stopping.
3. **Class Balancing**: Balanced class weighting applied to loss calculation to mitigate imbalance between categories.
4. **Exported to TFLite**: Converted using `tf.lite.TFLiteConverter` into an 8.6 MB portable model ready for edge and lightweight server deployment.

### Test Set Evaluation (452 test images):
```text
              precision    recall  f1-score   support

   cardboard      0.898     0.869     0.883        61
       glass      0.797     0.724     0.759        76
       metal      0.757     0.903     0.824        62
     organic      0.968     1.000     0.984        90
       paper      0.925     0.822     0.871        90
     plastic      0.818     0.863     0.840        73

    accuracy                          0.865       452
   macro avg      0.861     0.863     0.860       452
weighted avg      0.868     0.865     0.865       452
```

---

## 🚢 Production Deployment

To run in a production environment (e.g. AWS EC2, DigitalOcean, Ubuntu server):

### Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Systemd Service Configuration (Example)
Create `/etc/systemd/system/waste-classifier.service`:
```ini
[Unit]
Description=Go green Smart Waste Classifier
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/smart-waste-classifier
Environment="PATH=/home/ubuntu/smart-waste-classifier/venv/bin"
Environment="SECRET_KEY=your-secure-production-random-secret"
ExecStart=/home/ubuntu/smart-waste-classifier/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable waste-classifier
sudo systemctl start waste-classifier
```

Configure Nginx as a reverse proxy pointing to `http://127.0.0.1:5000`.

---

## 🔒 Configuration & Environment Variables

Key settings can be adjusted in [`config.py`](file:///home/md-asad-alam/all%20file/projects/smart-waste-classifier/config.py) or via environment variables:

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `"dev-only-change-me"` | Session secret key (set a strong random string in production) |
| `CONFIDENCE_THRESHOLD` | `0.60` (60%) | Minimum confidence needed for an "OK" status |
| `MAX_CONTENT_LENGTH` | `5 * 1024 * 1024` (5MB) | Maximum file upload size |
| `ALLOWED_EXTENSIONS` | `{"jpg", "jpeg", "png"}` | Permitted image file formats |

---

## ⚠️ Limitations & Notes

* **Single-item focus**: The model is an image-level classifier designed to identify a single dominant item per frame. Photos with multiple overlapping items may result in lower confidence.
* **Visual similarity**: Transparent plastics and clear glassware share visual characteristics and can occasionally be confused under certain lighting conditions.
* **Local regulation variation**: Waste segregation laws and municipal collection capabilities differ by city and country. The app's recommendations serve as general best-practice guidance.

---

## 📄 License & Attribution

Developed with ❤️ for a cleaner, greener planet. Feel free to use, fork, and improve this project!

