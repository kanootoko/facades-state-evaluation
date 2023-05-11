"""
List all images at the given directory, shuffle it and split to 3 files: train.txt, validate.txt and test.txt.
"""
from pathlib import Path
import random

TRAIN_PART = 0.7
VALIDATE_PART = 0.2
TEST_PART = 0.1

images_path = Path("./dataset/images")
output_dir = Path("./dataset")

TRAIN_PART, VALIDATE_PART, TEST_PART = (
    TRAIN_PART / (TRAIN_PART + VALIDATE_PART + TEST_PART),
    TEST_PART / (TRAIN_PART + VALIDATE_PART + TEST_PART),
    VALIDATE_PART / (TRAIN_PART + VALIDATE_PART + TEST_PART),
)

images = [file.name for file in images_path.iterdir() if file.name.lower().endswith(("jpg", "jpeg", "png"))]

random.shuffle(images)

t_v_point = int(len(images) * TRAIN_PART)
v_t_point = t_v_point + int(len(images) * VALIDATE_PART)
train = images[:t_v_point]
validate = images[t_v_point:v_t_point]
test = images[v_t_point:]

print(f"Got {len(train)} images to train, {len(validate)} for validation and {len(test)} to test")

(output_dir / "train.txt").write_text("\n".join(str(images_path / fname) for fname in sorted(train)))
(output_dir / "validate.txt").write_text("\n".join(str(images_path / fname) for fname in sorted(validate)))
(output_dir / "test.txt").write_text("\n".join(str(images_path / fname) for fname in sorted(test)))
