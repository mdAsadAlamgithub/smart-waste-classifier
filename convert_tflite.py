import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model("model/waste_classifier.keras")
tflite_bytes = tf.lite.TFLiteConverter.from_keras_model(model).convert()
with open("model/waste_classifier.tflite", "wb") as f:
    f.write(tflite_bytes)

# Check that it matches the Keras model
interp = tf.lite.Interpreter(model_content=tflite_bytes)
interp.allocate_tensors()
inp = interp.get_input_details()[0]
out = interp.get_output_details()[0]
x = np.random.randint(0, 256, (1, 224, 224, 3)).astype("float32")
interp.set_tensor(inp["index"], x)
interp.invoke()
print("Max difference vs Keras:", np.abs(interp.get_tensor(out["index"]) - model.predict(x, verbose=0)).max())
print("Size (MB):", round(len(tflite_bytes) / 1e6, 1))