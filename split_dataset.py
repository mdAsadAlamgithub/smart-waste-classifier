import os, random, shutil

random.seed(42)
src = "dataset_raw"
dst = "dataset"
splits = {"train": 0.70, "validation": 0.15, "test": 0.15}

for cls in os.listdir(src):
    cls_path = os.path.join(src, cls)
    if not os.path.isdir(cls_path):
        continue
    files = [f for f in os.listdir(cls_path)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(files)

    n = len(files)
    n_train = int(n * splits["train"])
    n_val = int(n * splits["validation"])
    parts = {
        "train": files[:n_train],
        "validation": files[n_train:n_train + n_val],
        "test": files[n_train + n_val:],
    }
    for split, items in parts.items():
        out = os.path.join(dst, split, cls)
        os.makedirs(out, exist_ok=True)
        for f in items:
            shutil.copy(os.path.join(cls_path, f), os.path.join(out, f))
    print(cls, {k: len(v) for k, v in parts.items()})