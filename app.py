import os
from pathlib import Path
import torch
import torch.nn as nn
from utils.Img2vec import Img2VecResnet18
from fastapi import FastAPI
from PIL import Image
import json
import shutil

app = FastAPI(title='Walpaper Rescomendation System')
device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
model = Img2VecResnet18(device=device)

with open(Path('data/allvectors.pt'), 'rb') as file:
    allvectors = torch.load(file)

with open(Path('data/catalog.json'), 'r', encoding='utf-8') as file:
    catalog = json.load(file)

if not os.path.exists(Path('data/rec')):
    os.mkdir(Path('data/rec'))

for folder, _, files in os.walk(Path('data/test')):
    for image in files:
        I = Image.open(Path(os.path.join(folder, image)))
        vec = model.getVec(I)
        vec = vec.unsqueeze(dim=0).to('cpu')
        cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        dist = cos(allvectors, vec)
        pdist, idx = torch.sort(dist, descending=True)
        idx = idx.tolist()[:]
        st = set()
        for i in idx:
            dct = catalog[i]
            for name in dct:
                value = dct[name]
                if tuple(value) not in st:
                    st.add(tuple(value))
                    path = Path(os.path.join('data/images', name))
                    # im = Image.open(path)
                    # # show image
                    # im.show()
                    shutil.copy(path, os.path.join('data/rec', name))
            if len(st) > 5:
                break
