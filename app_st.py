import streamlit as st
import os
from PIL import Image
import torch
from utils.Img2vec import Img2VecResnet18
from pathlib import Path
import json
import torch.nn as nn

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

# st.title('Fashion Recommender System')

# def save_uploaded_file(uploaded_file):
#     try:
#         with open(os.path.join('uploads',uploaded_file.name),'wb') as f:
#             f.write(uploaded_file.getbuffer())
#         return 1
#     except:
#         return 0
#
# def feature_extraction(img_path,model):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     expanded_img_array = np.expand_dims(img_array, axis=0)
#     preprocessed_img = preprocess_input(expanded_img_array)
#     result = model.predict(preprocessed_img).flatten()
#     normalized_result = result / norm(result)
#
#     return normalized_result
#
# def recommend(features,feature_list):
#     neighbors = NearestNeighbors(n_neighbors=6, algorithm='brute', metric='euclidean')
#     neighbors.fit(feature_list)
#
#     distances, indices = neighbors.kneighbors([features])
#
#     return indices
#
# # steps
# # file upload -> save
# uploaded_file = st.file_uploader("Choose an image")
# if uploaded_file is not None:
#     if save_uploaded_file(uploaded_file):
#         # display the file
#         display_image = Image.open(uploaded_file)
#         st.image(display_image)
#         # feature extract
#         features = feature_extraction(os.path.join("uploads",uploaded_file.name),model)
#         #st.text(features)
#         # recommendention
#         indices = recommend(features,feature_list)
#         # show
#         col1,col2,col3,col4,col5 = st.beta_columns(5)
#
#         with col1:
#             st.image(filenames[indices[0][0]])
#         with col2:
#             st.image(filenames[indices[0][1]])
#         with col3:
#             st.image(filenames[indices[0][2]])
#         with col4:
#             st.image(filenames[indices[0][3]])
#         with col5:
#             st.image(filenames[indices[0][4]])
#     else:
#         st.header("Some error occured in file upload")