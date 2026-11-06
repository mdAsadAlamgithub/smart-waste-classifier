import json
import threading
import numpy as np
from PIL import Image, ImageOps
import config

try:                                            # lightweight runtime (server)
    from ai_edge_litert.interpreter import Interpreter
except ImportError:
    try:
        from tflite_runtime.interpreter import Interpreter
    except ImportError:                         # your Windows PC
        import tensorflow as tf
        Interpreter = tf.lite.Interpreter

_interp = None
_classes = None
_lock = threading.Lock()                        # the interpreter is not thread-safe


def load():
    global _interp, _classes
    if _interp is None:
        _interp = Interpreter(model_path=config.TFLITE_PATH)
        _interp.allocate_tensors()
        with open(config.CLASSES_PATH) as f:
            _classes = json.load(f)
    return _interp, _classes


def preprocess(path):
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB").resize((224, 224))
    # No extra normalization: the model has its own Rescaling layer.
    return np.expand_dims(np.array(img, dtype="float32"), axis=0)


def predict(path, top_k=3):
    interp, classes = load()
    x = preprocess(path)
    with _lock:
        inp = interp.get_input_details()[0]
        out = interp.get_output_details()[0]
        interp.set_tensor(inp["index"], x)
        interp.invoke()
        probs = interp.get_tensor(out["index"])[0].copy()
    order = np.argsort(probs)[::-1][:top_k]
    return [{"label": classes[i], "confidence": float(probs[i])} for i in order]