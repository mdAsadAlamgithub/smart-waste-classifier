import json
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps
import config

_model = None
_classes = None


def load():
    """Load the model once and reuse it for every request."""
    global _model, _classes
    if _model is None:
        _model = tf.keras.models.load_model(config.MODEL_PATH)
        with open(config.CLASSES_PATH) as f:
            _classes = json.load(f)
    return _model, _classes


def preprocess(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)        # fixes rotated phone photos
    img = img.convert("RGB").resize((224, 224))
    # No extra normalization: the model has its own Rescaling layer.
    return np.expand_dims(np.array(img, dtype="float32"), axis=0)


def predict(path, top_k=3):
    model, classes = load()
    probs = model.predict(preprocess(path), verbose=0)[0]
    order = np.argsort(probs)[::-1][:top_k]
    return [{"label": classes[i], "confidence": float(probs[i])} for i in order]