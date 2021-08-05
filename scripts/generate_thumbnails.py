from csv import Sniffer
import glob
from os import path, mkdir
from PIL import Image


CAPTURE_DIR = glob.glob("/home/eddie/all_captures/**", recursive=True)
THUMBNAIL_DIR = path.abspath("./snapshots")
THUMBNAIL_WIDTH = 200

if not path.exists(THUMBNAIL_DIR):
    mkdir(THUMBNAIL_DIR)


for image_path in CAPTURE_DIR:
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
