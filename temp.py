import os
from pathlib import Path
import json
import shutil

path = Path('data/images')
pathnew = Path('data/new_images')

# for root, _, files in os.walk(path):
#     for file in files:
#         newname = file.split('_')[-1]
#         os.rename(os.path.join(root, file), os.path.join(root, newname))

with open(Path('catalog/catalog.json'), 'r', encoding='utf-8') as file:
    catalog = json.load(file)


for dct in catalog:
    for key in dct:
        shutil.copy(os.path.join(path, key), os.path.join(pathnew, key))

