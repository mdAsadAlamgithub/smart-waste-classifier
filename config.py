import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "waste_classifier.keras")
CLASSES_PATH = os.path.join(BASE_DIR, "model", "class_names.json")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024   # 5 MB
CONFIDENCE_THRESHOLD = 0.60            # tune after real-photo testing