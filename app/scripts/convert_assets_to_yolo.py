import os
import shutil

BASE_INPUT = "assets/mobs"
OUT_IMAGES = "dataset/images/train"
OUT_LABELS = "dataset/labels/train"
DATA_YAML = "dataset/data.yaml"

os.makedirs(OUT_IMAGES, exist_ok=True)
os.makedirs(OUT_LABELS, exist_ok=True)

classes = []
for class_id, class_name in enumerate(sorted(os.listdir(BASE_INPUT))):
    class_dir = os.path.join(BASE_INPUT, class_name)
    if not os.path.isdir(class_dir):
        continue

    classes.append(class_name)
    for fname in os.listdir(class_dir):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        src_path = os.path.join(class_dir, fname)
        dst_img = os.path.join(OUT_IMAGES, fname)
        dst_lbl = os.path.join(OUT_LABELS, os.path.splitext(fname)[0] + ".txt")

        shutil.copyfile(src_path, dst_img)

        with open(dst_lbl, "w") as f:
            f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

os.makedirs("dataset", exist_ok=True)
with open(DATA_YAML, "w") as f:
    f.write("path: C:/Users/samue/Documents/bot_rune/dataset\n")
    f.write("train: images/train\n")
    f.write("val: images/train\n")
    f.write("names:\n")
    for i, name in enumerate(classes):
        f.write(f"  {i}: {name}\n")

print(f"✅ Dataset YOLO gerado com {len(classes)} classes.")
