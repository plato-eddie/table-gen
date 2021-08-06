import os
from shutil import copyfile

FOLDER_290_CAPTURES = "/home/eddie/2_all_captures/290"
FOLDER_335_CAPTURES = "/home/eddie/2_all_captures/335"


def convert_290():
    for path, folders, files in os.walk(FOLDER_290_CAPTURES):
        for folder in folders:
            folder_path = os.path.join(path, folder)
            files = [
                f
                for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(".jpg")
            ]
            copyfile(
                os.path.join(folder_path, files[-1]),
                os.path.join(path, f"{folder}_290.jpg"),
            )
        break


def convert_335():
    for path, folders, files in os.walk(FOLDER_335_CAPTURES):
        files.sort()
        prefixes = set()
        for fil in files:
            fil_list = fil.split("_")
            prefix = fil_list[0]
            ext = fil.split('.')[-1]
            if prefix not in prefixes:
                os.rename(os.path.join(path, fil), os.path.join(path, f"{prefix}_narrow_335.{ext}"))
                prefixes.add(fil_list[0])
            else:
                os.rename(os.path.join(path, fil), os.path.join(path, f"{prefix}_wide_335.{ext}"))
        break


if __name__ == "__main__":
    convert_290()
    convert_335()
