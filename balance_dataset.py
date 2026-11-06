import os, random, shutil

random.seed(42)

src = "dataset_raw/organic"
backup = "dataset_extra/organic"
target = 600

os.makedirs(backup, exist_ok=True)

files = [f for f in os.listdir(src)
         if f.lower().endswith((".jpg", ".jpeg", ".png"))]
print("Organic before:", len(files))

if len(files) > target:
    random.shuffle(files)
    extra = files[target:]
    for f in extra:
        shutil.move(os.path.join(src, f), os.path.join(backup, f))

print("Organic after:", len(os.listdir(src)))
print("Moved to backup:", len(os.listdir(backup)))