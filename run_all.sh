#!/bin/sh
cd "$(dirname "$0")"

# MAKE SURE YOU SET ALL THE CONSTANTS CORRECTLY!

poetry shell
python3 convert_290.py
python3 generate_thumbnails.py
