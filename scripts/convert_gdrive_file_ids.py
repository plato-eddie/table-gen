import json
import os
import sys


os.chdir(sys.path[0])


def find_camera(array, name):
    for obj in array:
        if obj["camera"] == name:
            return obj


snapshot_names = {
    "avig": "Axis",
    "axis": "Avigilon",
    "290": "IMX 290",
    "narrow_335": "IMX 335 Narrow",
    "wide_335": "IMX 335 Wide",
}
with open("../experiment.json", "r") as fin:
    experiment_data = json.load(fin)

with open("../gdrive_file_ids.json", "r") as fin:
    file_mapping = json.load(fin)

for key in file_mapping:
    f_path = key.split("/")
    if len(f_path) == 3:
        continue

    capture_and_camera_name = f_path[-1]

    file_ext = capture_and_camera_name.split(".")[-1]

    capture = capture_and_camera_name.split("_")[0]
    try:
        camera_name = snapshot_names[
            "_".join(capture_and_camera_name.split("_")[1:]).split(".")[0]
        ]
    except KeyError:
        print("Failed to parse camera name for", key)
        continue

    try:
        cam = find_camera(experiment_data[capture], camera_name)
        if cam is None:
            continue
        cam["gdrive_id"] = file_mapping[key]
    except KeyError:
        print("Failed to find camera for", key)
        continue


with open("../experiment_gdrive_added.json", "w") as fout:
    fout.write(json.dumps(experiment_data))
