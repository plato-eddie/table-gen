import glob
from os import path, mkdir, chdir
from PIL import Image
import sys


chdir(sys.path[0])
CAPTURE_DIR = "/home/eddie/2_all_captures"
CAPTURE_DIRS = glob.glob(f"{CAPTURE_DIR}/**", recursive=True)
THUMBNAIL_DIR = path.abspath("../snapshots")
THUMBNAIL_WIDTH = 300

if not path.exists(THUMBNAIL_DIR):
    mkdir(THUMBNAIL_DIR)


for image_path in CAPTURE_DIRS:
    if image_path.lower().endswith(".jpg"):
        im = Image.open(image_path)
        im_ratio = im.height / im.width
        thumbnail_dim = (THUMBNAIL_WIDTH, im_ratio * THUMBNAIL_WIDTH)
        im.thumbnail(thumbnail_dim)
        im.save(
            path.join(
                THUMBNAIL_DIR, f"thumbnail_{path.basename(path.normpath(image_path))}"
            )
        )

