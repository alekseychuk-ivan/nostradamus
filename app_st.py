import streamlit as st
import os
from PIL import Image
import torch
from utils.Img2vec import Img2VecResnet18
from pathlib import Path
import json
import torch.nn as nn
import numpy as np

model = Img2VecResnet18()

st.title('Walpaper Recommender System')

with open(Path('data/catalog.json'), 'r', encoding='utf-8') as file:
    catalog = json.load(file)
with open(Path('data/allvectors.pt'), 'rb', ) as file:
    tensor = torch.load(file)
with open(Path('data/catalog_arteks.json'), 'r', encoding='utf-8') as file:
    catalog_arteks = json.load(file)


def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('data/test', uploaded_file.name), 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return 1
    except:
        return 0


def recommend(vec, feature_list, device='cpu'):
    vec = vec.unsqueeze(dim=0).to(device)
    cos = nn.CosineSimilarity(dim=1, eps=1e-6)
    dist = cos(feature_list, vec)
    pdist, idx = torch.sort(dist, descending=True)

    return idx


# steps
# file upload -> save
uploaded_file = st.file_uploader("Choose an image")
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):

        # display the file
        display_image = Image.open(uploaded_file)
        st.image(display_image)

    # feature extract
        features = model.getVec(display_image)
        # st.text(features)

        # recommendation
        indices = recommend(features, tensor).tolist()[:1]

        # show
        col1 = st.columns(1)  # col2, col3, col4, col5
        for i, idx in enumerate(indices):
            print(i, idx)
            dct = catalog[idx]
            name = list(dct.keys())[0]
            with col1:
                display_image = Image.open(os.path.join('data/images', name))
                st.image(np.asarray(display_image))
    else:
        st.header("Some error occured in file upload")
