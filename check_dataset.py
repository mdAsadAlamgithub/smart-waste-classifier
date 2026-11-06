import os
from PIL import Image

root = "dataset_raw"
bad = 0

for cls in sorted(os.listdir(root)):
    folder = os.path.join(root, cls)
    if not os.path.isdir(folder):
        continue
    good = 0
    for f in os.listdir(folder):
        path = os.path.join(folder, f)
        try:
            with Image.open(path) as img:
                img.verify()
            good += 1
        except Exception:
            bad += 1
            print("Corrupt:", path)
    print(f"{cls:10s} {good} valid images")

print("Corrupt files:", bad)