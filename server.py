from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import torch
from PIL import Image
from io import BytesIO
import json
from pathlib import Path
from utils.Img2vec import Img2VecResnet18, recommend
from typing import Union


app = FastAPI(title='Wallpapers recommendation system.')

model = Img2VecResnet18()


with open(Path('data/catalog.json'), 'r', encoding='utf-8') as file:
    catalog = json.load(file)
with open(Path('data/allvectors.pt'), 'rb', ) as file:
    tensor = torch.load(file)
with open(Path('data/catalog_arteks.json'), 'r', encoding='utf-8') as file:
    catalog_arteks = json.load(file)


@app.get('/')
async def home(request: Request):
    """ Returns barebones HTML form allowing the user to select a file and model """

    html_content = '''
    <form method="post" enctype="multipart/form-data">
        <div>
            <label>Upload Image</label>
            <input name="file" type="file" multiple>
                <div>
                    <label>Select Net Model</label>
                        <select name="model_name">
                            <option>Resnet18</option>                            
                        </select>                       
                </div>
                <div>
                    <label>Select Number of image</label>
                        <select name="number">
                            <option>5</option>                            
                        </select> 
                </div>
        </div>
        <button type="submit">Submit</button>
    </form>
    '''
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/")
async def process_home_form(file: UploadFile = File(...),
                            # model_name: str = Form(...),
                            number: int = Form(...)):
    """
    Requires an image file upload, model name.
    Returns: json response with list of list.
      Each list contains partnumber and collection of wallpaper.
    """
    # extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    # if not extension:
    #     return {'Error': 'Image must be jpg or png format!'}
    # else:
    # This is how you decode + process image with PIL
    features = model.getVec(Image.open(BytesIO(await file.read())))
    indices = recommend(features, tensor).tolist()
    st = set()
    for i in indices:
        if len(st) > number - 1:
            break
        dct = catalog[i]
        for name in dct:
            value = dct[name]
            if tuple(value) not in st:
                st.add(tuple(value))

    return st
