import sys, json
import numpy as np
import tensorflow as tf
from PIL import Image

model = tf.keras.models.load_model("model/waste_classifier.keras")
classes = json.load(open("model/class_names.json"))

for path in sys.argv[1:]:
    img = Image.open(path).convert("RGB").resize((224, 224))
    arr = np.expand_dims(np.array(img, dtype="float32"), axis=0)
    probs = model.predict(arr, verbose=0)[0]
    top = np.argsort(probs)[::-1][:3]
    print(path)
    for i in top:
        print(f"   {classes[i]:10s} {probs[i]*100:5.1f}%")