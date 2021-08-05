import os
from shutil import copyfile
FOLDER_290_CAPTURES = "/home/eddie/all_captures/recordings-290"

for path, folders, files in os.walk(FOLDER_290_CAPTURES):
    for folder in folders:
        folder_path = os.path.join(path, folder)
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.jpg')]
        copyfile(os.path.join(folder_path, files[-1]), os.path.join(path, f'{folder}_290.jpg'))
    break
