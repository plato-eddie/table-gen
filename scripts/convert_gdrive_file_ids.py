import json
import os
import sys


os.chdir(sys.path[0])

def find_camera(array, name):
    for obj in array:
        if obj['camera'] == name:
            return obj


with open("../experiment.json", "r") as fin:
    experiment_data = json.load(fin)

with open("../gdrive_file_ids.json", "r") as fin:
    file_mapping = json.load(fin)

for key in file_mapping:
    f_path = key.split("/")

    capture_and_camera_name = f_path[-1]

    file_ext = capture_and_camera_name.split(".")[-1]
    if file_ext != "jpg":
            continue

    if f_path[0] != "290":


        capture = capture_and_camera_name.split("_")[0]
        camera_name = "_".join(capture_and_camera_name.split("_")[1:]).split(".")[0]


        cam['gdrive_id'] = file_mapping[key]
    
    elif capture_and_camera_name == '00019.jpg':
        capture = f_path[1]
        camera_name = 'Avigilon'
    else:
        continue

    try:    
        cam = find_camera(experiment_data[capture], camera_name)
        if cam is None:
            continue
    except KeyError:
        continue
