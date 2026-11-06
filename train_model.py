import os, json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- Settings ----------
DATA_DIR = "dataset"
IMG_SIZE = (224, 224)
BATCH = 32
EPOCHS_HEAD = 15
EPOCHS_FINE = 10
UNFREEZE_LAST = 30
MODEL_PATH = "model/waste_classifier.keras"
CLASSES_PATH = "model/class_names.json"

os.makedirs("model", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
tf.keras.utils.set_random_seed(42)

# ---------- Data ----------
def load(split, shuffle):
    return tf.keras.utils.image_dataset_from_directory(
        f"{DATA_DIR}/{split}",
        image_size=IMG_SIZE,
        batch_size=BATCH,
        label_mode="categorical",
        shuffle=shuffle,
        seed=42,
    )

train_ds = load("train", True)
val_ds = load("validation", False)
test_ds = load("test", False)

class_names = train_ds.class_names
n_classes = len(class_names)
print("Class order:", class_names)

with open(CLASSES_PATH, "w") as f:
    json.dump(class_names, f)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

# ---------- Class weights ----------
counts = [len(os.listdir(f"{DATA_DIR}/train/{c}")) for c in class_names]
y_train = np.concatenate([[i] * n for i, n in enumerate(counts)])
weights = compute_class_weight("balanced", classes=np.arange(n_classes), y=y_train)
class_weight = dict(enumerate(weights))
print("Class weights:", {class_names[i]: round(w, 2) for i, w in class_weight.items()})

# ---------- Model ----------
augment = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.15),
    layers.RandomBrightness(0.2),
    layers.RandomContrast(0.2),
], name="augmentation")

base = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet"
)
base.trainable = False

inputs = layers.Input(shape=IMG_SIZE + (3,))
x = augment(inputs)
x = layers.Rescaling(1.0 / 127.5, offset=-1)(x)   # MobileNetV2 preprocessing built in
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(n_classes, activation="softmax")(x)
model = models.Model(inputs, outputs)

def callbacks():
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.3, patience=2, min_lr=1e-7),
    ]

# ---------- Phase A: train the new head ----------
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy", metrics=["accuracy"])
print("\n=== Phase A: training classification head ===")
h1 = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_HEAD,
               class_weight=class_weight, callbacks=callbacks())
head_val_acc = model.evaluate(val_ds, verbose=0)[1]
head_weights = model.get_weights()

# ---------- Phase B: fine-tune top layers ----------
base.trainable = True
for layer in base.layers[:-UNFREEZE_LAST]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss="categorical_crossentropy", metrics=["accuracy"])
print("\n=== Phase B: fine-tuning ===")
h2 = model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS_FINE,
               class_weight=class_weight, callbacks=callbacks())
fine_val_acc = model.evaluate(val_ds, verbose=0)[1]

if fine_val_acc < head_val_acc:
    print("Fine-tuning did not help; keeping head-only weights.")
    model.set_weights(head_weights)
print(f"Validation accuracy: head={head_val_acc:.4f}, fine-tuned={fine_val_acc:.4f}")

model.save(MODEL_PATH)
print("Saved:", MODEL_PATH)

# ---------- Training curves ----------
acc = h1.history["accuracy"] + h2.history["accuracy"]
val = h1.history["val_accuracy"] + h2.history["val_accuracy"]
loss = h1.history["loss"] + h2.history["loss"]
vloss = h1.history["val_loss"] + h2.history["val_loss"]
split_at = len(h1.history["accuracy"])

fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(acc, label="train"); ax[0].plot(val, label="validation")
ax[0].axvline(split_at - 1, ls="--", c="gray"); ax[0].set_title("Accuracy"); ax[0].legend()
ax[1].plot(loss, label="train"); ax[1].plot(vloss, label="validation")
ax[1].axvline(split_at - 1, ls="--", c="gray"); ax[1].set_title("Loss"); ax[1].legend()
plt.tight_layout(); plt.savefig("outputs/training_curves.png", dpi=150); plt.close()

# ---------- Final test evaluation ----------
probs = model.predict(test_ds, verbose=0)
y_pred = np.argmax(probs, axis=1)
y_true = np.concatenate([np.argmax(y, axis=1) for _, y in test_ds])

report = classification_report(y_true, y_pred, target_names=class_names, digits=3)
print("\n=== Test set results ===\n", report)
with open("outputs/classification_report.txt", "w") as f:
    f.write(report)

cm = confusion_matrix(y_true, y_pred)
fig, ax = plt.subplots(figsize=(7, 6))
ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(n_classes)); ax.set_xticklabels(class_names, rotation=45, ha="right")
ax.set_yticks(range(n_classes)); ax.set_yticklabels(class_names)
for i in range(n_classes):
    for j in range(n_classes):
        ax.text(j, i, cm[i, j], ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black")
ax.set_xlabel("Predicted"); ax.set_ylabel("Actual"); ax.set_title("Confusion matrix")
plt.tight_layout(); plt.savefig("outputs/confusion_matrix.png", dpi=150); plt.close()
print("Saved charts to outputs/")