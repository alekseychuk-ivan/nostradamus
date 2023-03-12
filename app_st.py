import streamlit as st
import os
from PIL import Image
import torch
from utils.Img2vec import Img2VecResnet18, recommend
from pathlib import Path
import json
import torch.nn as nn

model = Img2VecResnet18()

st.title('Wallpapers Recommender System')
if not os.path.exists(Path('data/images')):
    Path('data/test').mkdir(parents=True)

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
        indices = recommend(features, tensor).tolist()

        # show
        col = st.columns(5, gap='small')  # col2, col3, col4, col5
        i = 0
        dataset = set()
        for idx in indices:
            if i > 4:
                break
            dct = catalog[idx]
            name = list(dct.keys())[0]
            col_data = dct[name]
            if tuple(col_data) not in dataset:
                dataset.add(tuple(col_data))
                with col[i]:
                    i += 1
                    display_image = Image.open(os.path.join('data/images', name))
                    st.text(f'{col_data[1]}, {col_data[0]}')
                    # st.text(f'номер {col_data[0]}')
                    st.image(display_image)
    else:
        st.header("Some error occured in file upload")
